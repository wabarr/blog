from django.forms import ModelForm, inlineformset_factory
from blog.models import CompositePost, Block

class CompositePostForm(ModelForm):
    class Meta:
        model = CompositePost
        fields = ['title', 'slug','author','category','map_latitude','map_longitude','map_popup_label']

BlockFormset = inlineformset_factory(
    parent_model=CompositePost,
    model=Block,
    fields=['content', 'post', 'img', 'sort_order'],
    extra=1,            # Number of empty form fields to show by default
    can_delete=True     # Allows users to mark existing children for deletion
)