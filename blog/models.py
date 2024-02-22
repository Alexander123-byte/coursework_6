from django.db import models


class Blog(models.Model):
    """Модель блога"""
    title = models.CharField(max_length=150, verbose_name='название')
    slug = models.CharField(max_length=150, verbose_name='slug', blank=True, null=True)
    content = models.TextField(verbose_name='содержание')
    preview = models.ImageField(upload_to='image/', verbose_name='изображение', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='признак публикации', default=True)
    view_count = models.IntegerField(verbose_name='количество просмотров', default=0)

    def __str__(self):
        return f'{self.title} {self.create_date} {self.is_published}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('create_date',)
