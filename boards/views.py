from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from boards.forms import NewTopicForm, PostForm, EditPostForm
from .models import Board, Post, Topic
from .serializers import BoardSerializer


def home(request):
    boards = Board.objects.all()
    print(boards)
    return render(request, 'home.html', {'all_boards': boards})


# Dynamic URL
# Open Topic
def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'topics.html', {"board": board})


# Create New Topic
@login_required
def create_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    user = User.objects.first()

    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)  # Start Get Data
            topic.board = board
            topic.created_by = user
            topic.save()  # Save Topic into Databases

            # Save Post into DB
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=user,
                topic=topic
            )

            return redirect('board_topics', board_id=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {"board": board, "form": form})


# Dynamic URL
# Open Topic
def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    # Updating View using Session
    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True
    return render(request, 'topic_posts.html', {"topic": topic})


# Reply For Topic
# Using login_required, will send the user to login page if not logged in
@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Start Get Data
            post.topic = topic
            post.created_by = request.user
            post.save()  # Save Post into Databases

            return redirect('topic_posts', board_id=board_id, topic_id=topic.id)
    else:
        form = PostForm()

    return render(request, 'reply_topic.html', {"topic": topic, 'form': form})


# Updating Reply
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    topic = Topic.objects.get(pk=post.topic_id)
    board = Board.objects.get(pk=topic.board_id)

    if request.method == "POST":
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('topic_posts', board_id=board.id, topic_id=topic.id)
    else:
        form = EditPostForm(instance=post)

    return render(request, 'edit_post.html', {"post": post, 'form': form})


# Testing APIs,
# Using REST Framework
def boards_list(request):  # All Boards
    boards = Board.objects.all()
    data = {'Results': list(boards.values("id", "name", "description", "topics__subject"))}
    return JsonResponse(data)


def boards_list_id(request, board_id):  # Specific Board
    board = get_object_or_404(Board, pk=board_id)
    data = {'Results': {
        "id": board.id,
        "name": board.name,
        "description": board.description
    }}
    return JsonResponse(data)


# Testing Functions in API
def increment_by(request, first, increment):
    ans = first + increment
    data = {'Result': {
        "Number": first,
        "Increment": increment,
        "Sum": ans
    }}
    return JsonResponse(data)


# Testing
# GET and POST, Return JSON Response
# http://127.0.0.1:8000/apis/test/
@api_view(['GET', 'POST'])
def apiOverview(request):
    if request.method == 'GET':
        return JsonResponse("[GET]: API WORKS", safe=False)
    if request.method == 'POST':
        return JsonResponse("[POST]: API WORKS", safe=False)


# Testing 2
# GET
# REST Response (Returning a Json Format)
@api_view(['GET'])
def apiOverview_2(request):
    api_urls = {
        'List': '/board/list/',
        'Detail': '/board/list/<int:pk>',
        'Create': '/board/create/',
        'Delete': '/board/delete/<int:pk>',
        # 'Update': '/board/update/<int:pk>'
    }
    return Response(api_urls)


# Testing 3  (LIST ALL BOARDS)
# Serializers to Return Model in JSON
@api_view(['GET'])
def board_list(request):
    boards = Board.objects.all()
    # Convert to Json Format using Serializer
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)


# Testing 4  (SHOW Details of One BOARD)
# Serializers to Return Model in JSON
@api_view(['GET'])
def board_detail(request, pk):
    board = Board.objects.get(id=pk)
    # Convert to Json Format using Serializer
    serializer = BoardSerializer(board, many=False)
    return Response(serializer.data)  # Testing 4  (SHOW Details of One BOARD)


# CREATE BOARD (POST)
@api_view(['POST'])
def board_create(request):
    serializer = BoardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# UPDATE BOARD (POST)
@api_view(['POST'])
def board_update(request, pk):
    board = Board.objects.get(id=pk)
    serializer = BoardSerializer(instance=board, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


# Testing Query Set Parameters   http://localhost:8000/apis/test/board-details-queryset?id=1
class BoardList(generics.ListCreateAPIView):
    model = Board
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.all()
        board_id = self.request.query_params.get('id')
        if board_id:
            queryset = queryset.filter(id=board_id)

        return queryset
