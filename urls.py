"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from blog.admin import BlogAdminSite, admin
from django.urls import path, include
from blog.views import  (HomeView, MapView, AboutView, CategoryView, CategoryListView,
                         login_view, PostDetailView, edit_composite_post, create_composite_post)


urlpatterns = [
    path('', HomeView.as_view(), name='home-list'),
    path("accounts/login/", login_view, name="login"),
    path('admin/', BlogAdminSite.urls),
    path('about/', AboutView.as_view()),
    path('map/', MapView.as_view()),
    path('categories/<category>/', CategoryView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("edit/<pk>/", edit_composite_post, name="manage-composite-post"),
    path("create/", create_composite_post, name="create-composite-post"),
    path('comments/', include('django_comments.urls')),
    path('su/',admin.site.urls),

]
