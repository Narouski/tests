from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    groups = get_object_or_404(Group, slug=slug)
    posts = groups.group_posts.all()[:12]
    return render(
        request,
        "group.html",
        {"group": groups, "posts": posts}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'profile.html',
        {'author': author,
         'paginator': paginator,
         'posts': posts,
         'page': page}
    )


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    author = post.author
    return render(
        request,
        'post.html',
        {'author': author,
         'post': post}
    )


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(
                "post",
                username=request.user.username,
                post_id=post_id)
    return render(
        request,
        'post_new.html',
        {'form': form, 'post': post},
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')
    return render(request, "post_new.html", {"form": form})
    form = PostForm()
    return render(request, "post_new.html", {"form": form})
