from django.contrib import admin
from django.db.models import Count

from .models import Tag, Article, Comment


class TagRatingFilter(admin.SimpleListFilter):
    title = 'Rating filter'
    parameter_name = 'tag_rating'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request).values().annotate(rating=Count('article')).order_by('title')
        types = qs.values_list('id', 'rating').order_by('rating')
        return tuple(types)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
        return queryset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'rating')
    readonly_fields = ('rating',)
    fields = ('title', 'slug', 'rating')
    list_filter = [TagRatingFilter]
    search_fields = ('title', 'slug')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'add_at', 'article', 'is_article_author')
    readonly_fields = ('author', 'add_at', 'article', 'is_article_author')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_at', 'update_at')
    readonly_fields = ('title', 'author', 'create_at')
