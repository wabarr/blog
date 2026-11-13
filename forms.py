from django.forms import ModelForm, inlineformset_factory
from blog.models import CompositePost, Block, BlogComment
from django import forms

class CompositePostForm(ModelForm):
    class Meta:
        model = CompositePost
        fields = ['title', 'slug','author','category','map_latitude','map_longitude','map_popup_label']

BlockFormset = inlineformset_factory(
    parent_model=CompositePost,
    model=Block,
    fields=['content', 'post', 'img', 'sort_order'],
    help_texts={'content':None},
    extra=0,            # Number of empty form fields to show by default
    can_delete=True     # Allows users to mark existing children for deletion
)
class BlogCommentForm(ModelForm):
    class Meta:
        model = BlogComment
        #exclude the post and user field because a user should never alter this
        #post will be handled in the view logic
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'What do you have to say?',
                'rows': 3,
            }),
        }
        labels = {
            'content': '',
        }
