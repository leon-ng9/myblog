from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render 
from django.utils import timezone
from .forms import PostForm
from .models import Post
import calendar

# Create your views here.

def mkmonth_lst():
    """Make a list of months to show archive links."""

    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    months = []
    for post in post_list:
        y = post.published_date.year
        m = post.published_date.month
        if (m not in [month[1] for month in months]):
            months.append((y, m, calendar.month_name[m]))

    return months

def post_list(request):
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list, 5) # number of posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts, 'months': mkmonth_lst()})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'months': mkmonth_lst()})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        save = request.POST.get("save", False)
        if save:
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        delete = request.POST.get("delete", False)
        if (delete):
            post.delete()
            return redirect('post_list')
        else:
            return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_delete.html', {})

def post_month(request, year, month):
    post_list = Post.objects.filter(published_date__year=year, published_date__month=month).order_by('-published_date')
    paginator = Paginator(post_list, 5) # number of posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_month.html', {'posts': posts, 'months': mkmonth_lst()})