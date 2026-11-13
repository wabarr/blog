from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from blog.models import  CompositePost, Category, BlogComment
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_not_required, permission_required
from blog.forms import BlockFormset, CompositePostForm, BlogCommentForm


class CategoryListView(ListView):
    model = Category

class CategoryView(ListView):
    model = CompositePost
    paginate_by = 100
    template_name = "blog/categories.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        return context
    def get_queryset(self):
        return CompositePost.objects.filter(category__name=self.kwargs['category'])

class PostDetailView(DetailView):
    model = CompositePost
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = BlogCommentForm()

        try:
            context['nextpost'] = self.object.get_next_by_published_date()
        except:
            pass
        try:
            context['prevpost'] = self.object.get_previous_by_published_date()
        except:
            pass
        try:
            context['comments'] = BlogComment.objects.filter(post=self.object.pk).order_by('-created')
        except:
            pass

        return(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = self.request.user
            #the post field is not included in the form so it needs to be added in here in the view
            comment.save()
            return redirect('post-detail', slug=self.object.slug)

        # If invalid, re-render the page with the object and form errors
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class MapView(TemplateView):
    template_name = "blog/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = CompositePost.objects.filter(map_latitude__isnull=False, map_longitude__isnull=False)
        return context

class HomeView(ListView):
    model = CompositePost
    paginate_by = 10
    template_name="blog/post_list.html"

@login_not_required
def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      urlForRedirect = request.GET.get('next')
      return redirect(urlForRedirect)
  else:
    form = AuthenticationForm()

  return render(request, "blog/login.html", {"form": form})

@permission_required('blog.add_composite_post')
def edit_composite_post(request, pk=None):
    composite_post = get_object_or_404(CompositePost, pk=pk) if pk else None
    if request.method == 'POST':
        form = CompositePostForm(request.POST, request.FILES, instance=composite_post)
        formset = BlockFormset(request.POST, request.FILES, instance=composite_post)

        # Check validation on BOTH the main form and formset
        if form.is_valid() and formset.is_valid():
            # Save the parent instance first
            parent_instance = form.save()

            # Associate the formset data with the saved parent and save children
            formset.instance = parent_instance
            formset.save()

            return redirect('/')  # Replace with your success URL
    else:
        form = CompositePostForm(instance=composite_post)
        formset = BlockFormset(instance=composite_post)

    context = {
        'form': form,
        'formset': formset,
        'is_edit': pk is not None
    }
    return render(request, 'blog/manage_composite_post.html', context)

@permission_required('blog.add_composite_post')
def create_composite_post(request):
    if request.method == 'POST':
        form = CompositePostForm(request.POST, request.FILES)
        formset = BlockFormset(request.POST, request.FILES)

        # Check validation on BOTH the main form and formset
        if form.is_valid() and formset.is_valid():
            # Save the parent instance first
            parent_instance = form.save()

            # Associate the formset data with the saved parent and save children
            formset.instance = parent_instance
            formset.save()

            return redirect('/')  # Replace with your success URL
    else:
        form = CompositePostForm()
        formset = BlockFormset()

    context = {
        'form': form,
        'formset': formset,
        'is_edit': False,
    }
    return render(request, 'blog/manage_composite_post.html', context)
