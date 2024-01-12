from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    
    # pagination with 2 posts per page
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # get first page if provided page number is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # get last page if the provided page number if out of range
        posts = paginator.page(paginator.num_pages)


    context = {
        'posts' : posts
    }
    return render(request, 
                  'blog/post/list.html', 
                  context)


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post_slug, 
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    context = {
        'post' : post
    }
    
    return render(request,
                  "blog/post/detail.html",
                  context)