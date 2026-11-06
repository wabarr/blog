from django.contrib import admin

from .models import CompositePost, Category, Block

from django_comments.models import Comment

class BlogAdminSite(admin.AdminSite):
    site_header = "Fentarr Blog Admin"

BlogAdminSite = BlogAdminSite(name='Blog Admin')

@admin.register(Category, site=BlogAdminSite)
class CategoryAdmin(admin.ModelAdmin):
    # What columns show up in the list view
    list_display = ('name', 'slug')
    # Automatically fills the slug as you type the name
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment, site=BlogAdminSite)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment",)

@admin.register(Block, site=BlogAdminSite)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


class BlockInline(admin.StackedInline):
    model = Block

@admin.register(CompositePost, site=BlogAdminSite)
class CompositePostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlockInline]


# @admin.register(Post, site=BlogAdminSite)
# class PostAdmin(admin.ModelAdmin):
#     # Columns to display in the admin list
#     list_display = ('title', 'author', 'published_date')
#
#     # Sidebar filters to help you find posts quickly
#     list_filter = ('category', 'author', 'published_date')
#
#     # Adds a search bar at the top
#     search_fields = ('title', 'content')
#
#     # Automatically fills the slug based on the title
#     prepopulated_fields = {'slug': ('title',)}
#
#     # Adds a nice date-based navigation bar at the top
#     date_hierarchy = 'published_date'
#
#     # Orders the list by date (newest first)
#     ordering = ('-published_date',)