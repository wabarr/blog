from django.contrib import admin

from .models import CompositePost, Category, Block, BlogComment


class BlogAdminSite(admin.AdminSite):
    site_header = "Fentarr Blog Admin"

BlogAdminSite = BlogAdminSite(name='Blog Admin')

@admin.register(Category, site=BlogAdminSite)
class CategoryAdmin(admin.ModelAdmin):
    # What columns show up in the list view
    list_display = ('name', 'slug')
    # Automatically fills the slug as you type the name
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogComment, site=BlogAdminSite)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("user","post", "created")

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
