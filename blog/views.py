from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    template_name = 'blog/post/post_list.html'
    context_object_name = 'posts'

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/post_list.html', {'page': page_obj, 'posts': posts, 'tag': tag})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            print('test')
            new_comment.save()
    else:
        comment_form = CommentForm()
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(tag_count=Count('tags')).order_by('-tag_count', '-publish')[:3]
    return render(request, 'blog/post/post_detail.html', {'post': post,
                                                          'comment_form': comment_form,
                                                          'comments': comments,
                                                          'new_comment': new_comment,
                                                          'similar_posts': similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(f'The message was send successfully!')
            # post_url = request.build_absolute_uri(post.get_absolute_url())
            # subject = '{} ({}) recommends you reading "; {}; "'.format(data['name'], data['email'], post.title)
            # message = 'Read "{}" at {}\n\n{}\'s comments:; {}; '.format(post.title, post_url, data[' '], data['; name; comments; '])
            # send_mail(subject, message, 'admin@myblog.com', [data['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})



