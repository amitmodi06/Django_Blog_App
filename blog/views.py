from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

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
        'posts' : posts,
        'tag' : tag
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
    comments = post.comments.filter(active=True)
    form = CommentForm()

    #Retrieving posts by similarty of tags
    #Regrieves tag ids for current post
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get all posts with these tags and exclude current post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Order posts with number of common tags and then published date and limit to 4 results
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'post' : post,
        'comments' : comments,
        'form' : form,
        'similar_posts' : similar_posts
    }
    
    return render(request,
                  "blog/post/detail.html",
                  context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, cd['email_from'], [cd['email_to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post' : post,
        'form' : form,
        'sent' : sent
    }

    return render(request,
                  'blog/post/share.html',
                  context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, 
                             id=post_id, 
                             status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        #Creating a comment object without saving it to the DB
        comment = form.save(commit=False)
        comment.post = post
        #Saving the comment to the DB
        comment.save()

    context = {
        'post' : post,
        'form' : form,
        'comment' : comment
    }

    return render(request,
                  'blog/post/comment.html',
                  context)