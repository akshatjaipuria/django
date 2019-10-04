from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from .models import Post
from accounts import views as accounts_views


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, 'home.html', {'posts': posts})
    else:
        return accounts_views.login(request)


def post(request, slug):
    if request.user.is_authenticated:
        return render_to_response('post.html', {
            'post': get_object_or_404(Post, slug=slug),
        })
    else:
        return accounts_views.login(request)
