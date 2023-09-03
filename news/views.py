from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from NewsPaper import settings
from .forms import AddPostForm
from .models import Post, Category
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-dateCreation'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    template_name = 'post_create.html'
    form_class = AddPostForm


    def post(self, request, *args, **kwargs):
        form = AddPostForm(request.POST)
        post_category_pk = request.POST['postCategory']
        sub_text = request.POST.get('text')
        sub_title = request.POST.get('title')
        post_category = Category.objects.get(pk=post_category_pk)
        subscribers = post_category.subscribers.all()

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

        for subscriber in subscribers:
            html_content = render_to_string(
                'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post, 'title': sub_title}
            )
            msg = EmailMultiAlternatives(
                subject=sub_title,
                body=f'{sub_text[:50]}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        return redirect('/news/')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    template_name = 'post_create.html'
    form_class = AddPostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post', )
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'personal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе authors
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    ordering = 'categoryName'
    paginate_by = 10


class CategoryDetail(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    ordering = 'categoryName'
    paginate_by = 10


class PostByCategoryListView(ListView):
    model = Post
    template_name = 'post_list_by_category.html'
    context_object_name = 'posts'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        queryset = Post.objects.all().filter(postCategory__pk=self.category.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoryName'] = self.category.categoryName
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
    

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = "Вы успешно подписались на рассылку новостей категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})
