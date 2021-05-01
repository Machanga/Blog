from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.
class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView): 
    model = Post
    template_name = 'post_detail.html'

class BlogCreateView(LoginRequiredMixin, CreateView): 
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})

