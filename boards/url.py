from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<int:board_id>/', views.board_topics, name='board_topics'),
    path('boards/<int:board_id>/new/', views.create_topic, name='create_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('boards/<int:board_id>/topics/<int:topic_id>/reply/', views.reply_topic, name='reply_topic'),
    path('boards/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('boards/boards_list', views.boards_list, name='boards_list'),
    path('boards/boards_list/<int:board_id>', views.boards_list_id, name='boards_list_id'),

    # Testing
    path('increment/<int:first>/<int:increment>', views.increment_by),

    # Testing API
    path('apis/test/', views.apiOverview, name='API_Test'),
    path('apis/test2/', views.apiOverview_2, name='API_Test2'),
    path('apis/test/board-list', views.board_list, name='board-list'),
    path('apis/test/board-detail/<int:pk>', views.board_detail, name='board-detail'),
    path('apis/test/board-create/', views.board_create, name='board-create'),
    path('apis/test/board-update/<int:pk>', views.board_update, name='board-update'),

    # Testing QuerySetParameters
    path('apis/test/board-details-queryset', views.BoardList.as_view(), name='board-update'),


]
