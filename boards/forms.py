from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    # Extra Fields:
    # We added a new field Message -> because it's not in the Topic Model,
    # so we have to add it independently
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': "what is in your mind?"}),
        max_length=4000,
        help_text="max length is 4000")

    # Fields inside The Model:
    class Meta:
        model = Topic
        fields = ['subject', 'message']


# Form For Adding a New Post (Reply)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']


# Form to Edit Post
class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
        labels = {
            'message': "New Reply",
        }
