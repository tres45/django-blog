from django.shortcuts import render
from django.views.generic.base import View

from .models import Comment, Tag, Article


class CommentsView(View):
    """Comments information"""
    def get(self, request):
        data = Comment.objects.all()
        return render(request, 'blog/comment.html', {'data': data})


class TagsView(View):
    """Tags information"""
    def get(self, request):
        data = Tag.objects.all()
        return render(request, 'blog/tag.html', {'data': data})


class ArticlesView(View):
    """Articles information"""
    def get(self, request):
        data = Article.objects.all()
        comment_statistics = Article.objects.comment_statistics()
        return render(request, 'blog/article.html', {'data': data, 'comment_statistics': comment_statistics})
