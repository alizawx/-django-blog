from email.policy import default
from itertools import count
from multiprocessing import context

from django.contrib.postgres.search import SearchVector, SearchQuery
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .forms import *
import datetime
from django.views.decorators.http import require_POST
from .models import Post
from django.db.models import Sum,Count
from .templatetags.blog_tags import total_post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth.decorators import login_required

# Create your views here.



def index(request):
    total_views = Post.published.aggregate(
        total=Sum('view_counts')
    )
    context = {
        'total_views': total_views['total']
    }
    return render(request, "blog/index.html", context)


def post_list(request):
    posts = Post.published.all()
    form = SearchForm()
    categories = Category.objects.annotate(post_count=Count('posts'))

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'form': form,
        'categories' :categories,
    }

    return render(request, "blog/list.html", context)


# class PostListView(ListView):
#     context_object_name = "posts"
#     queryset = Post.published.all()
#     paginate_by = 3
#     template_name = "blog/list.html"


def post_detail(request, pk):
    try:
        post = Post.published.get(id=pk)
    except Post.DoesNotExist:
        raise Http404("No post found")
    post.view_counts += 1
    post.save()
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'new_date': datetime.datetime.now(),
        'comments':comments,
    }
    return render(request, "blog/detail.html", context)

def category_posts(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug
    )
    posts = Post.published.filter(
        category__slug=slug
    )
    categories = Category.objects.annotate(
        post_count=Count('posts')
    )
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/list.html', context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = "blog/detail.html"

# def ticket(request):
#     ticket_obj = Ticket.objects.all()
#     if request.method =="POST":
#         form  = TicketForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             ticket_obj = Ticket()
#             ticket_obj.message = cd['message']
#             ticket_obj.name = cd['name']
#             ticket_obj.email = cd['email']
#             ticket_obj.phone = cd['phone']
#             ticket_obj.subject = cd['subject']
#             ticket_obj.save()
#             return redirect("index")
#
#         else:
#             form = TicketForm()
#             return render(request, 'blog/ticket.html',{'form':form})


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject']
            )
            return redirect("blog:index")
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
            'post': post,
            'comment': comment,
            'form': form
        }
    return  render(request,"forms/comment.html" ,context)

def author_detail(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    context = {
        'author': user,
        'posts': posts,
        'posts_count': posts.count(),
    }
    return render(request, 'blog/author_detail.html', context)


def searching(request):
    query = request.GET.get('q')

    if query:
        search_vector = (
                SearchVector('title', weight='A') +
                SearchVector('description', weight='B') +
                SearchVector('slug', weight='C')
        )
        search_query = SearchQuery(query)
        query_list = (
            Post.objects
            .annotate(
                search=search_vector,
                similarity=TrigramSimilarity('title', query),
                rank=SearchRank(search_vector, search_query),
            )
            .filter(similarity__gt=0.01)
            .order_by('-similarity')
        )

        # final_query = query_list.filter(search=search_query).order_by('-rank')
        final_query = query_list

        context = {
            'final_query':final_query ,
        }
        print(query_list.count())
        return render(request,'blog/search.html',context)

    else:
        final_query = Post.published.all()

        context = {
            'final_query':final_query,
        }

        return render(request, 'blog/search.html',context)


# def profile(request):
#     user = request.user
#     posts= Post.published.filter(author=user)
#
#     return render(request,"blog/profile.html" ,{"posts":posts})
@login_required(login_url='/admin/login/')
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/profile.html', {'posts': posts})


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.images.add(form.cleaned_data['image'])
            post.save()
            return redirect(' blog:index')
    else :
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form':form})