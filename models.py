from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.core.files.storage import storages
from bs4 import BeautifulSoup




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    legacy_WP_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Block(models.Model):
    content = CKEditor5Field('Text', config_name='default', null=True, blank=True, help_text='If there is an image defined, then any other content is ignored')
    #note related_name='blocks' allows you when you have a CompositePost object to say post.blocks
    post = models.ForeignKey('CompositePost', on_delete=models.CASCADE, related_name='blocks')
    img = models.ImageField(storage=storages['personal_blog_storage'], null=True, blank=True)
    sort_order = models.IntegerField()
    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        if self.img:
            return f"image block pk:{self.pk}"
        else:
            return f"content block pK={ self.pk }"


class CompositePost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compositeposts', limit_choices_to={'is_staff': True}, default=1)
    category = models.ManyToManyField(Category)
    map_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_popup_label = models.CharField(max_length=50, null=True, blank=True)

    # Date fields: published handles the actual date, created tracks the entry
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_first_img_url(self):
        #gets the signed URL for the first image in the blocks attached to a post
        for block in self.blocks.all():
            if block.img:
                return block.img.url

    def get_truncated_content(self):
        for block in self.blocks.all():
            if not block.img:
                soup = BeautifulSoup(block.content, 'html.parser')
                clean_text = soup.get_text()
                return clean_text[:150]
            else:
                pass
