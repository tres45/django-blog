from django.urls import path

from . import views


urlpatterns = [
    path('comments', views.CommentsView.as_view()),
    path('articles', views.ArticlesView.as_view()),
    path('tags', views.TagsView.as_view()),
]
