from datetime import date
from django.db import models
from django.urls import reverse
from antonio.settings import MEDIA_ROOT
from poems.service import FireBaseStorage
import os

class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    def get_absolute_url(self):
        return reverse('cat_poem', args=[self.slug])
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        
class PoemPublished(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Poem(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name="Заголовок")
    link_stih = models.CharField(blank=True, max_length=255, verbose_name="Ссылка на Стихи.ру")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    cats = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='poem', verbose_name='Категория',
                             null=True, blank=True)
    content = models.TextField(blank=True, verbose_name="Текст статьи", db_index=True)
    preview = models.ImageField(blank=True, upload_to="photos", verbose_name="Фото")
    photo = models.TextField(verbose_name='Внешняя ссылка на фото', blank=True)
    time_create = models.DateField(verbose_name="Время создания", default=date.today)
    time_update = models.DateField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Статус публикации")
    author = models.ForeignKey('auth.User', related_name='poems', on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()
    published = PoemPublished()
    count_view = models.IntegerField(blank=True, default=0, verbose_name="Всего просмотров")
    key_words = models.CharField(blank=True, max_length=255, verbose_name="Keywords")
    description = models.TextField(blank=True, max_length=255, verbose_name="Description")
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super(Poem, self).save(*args, **kwargs)
        try:
            if self.preview:
                namefile = self.preview.name.split('/')[-1]
                pathname = 'poems/photos/'
                pathname += f'{namefile}'
                self.photo = FireBaseStorage.get_publick_link(self.images_path, pathname)
                os.remove(self.images_path)
                super(Poem, self).save(*args, **kwargs)
        except BaseException as err:
            print(err)
    @property        
    def images_path(self):
        return os.path.join(MEDIA_ROOT, self.preview.name)
    @property
    def get_author(self):
        if self.author:
            return f'{self.author.first_name} {self.author.last_name}'
        return 'Нет'
    def get_absolute_url(self):
        return reverse('show_poem', args=[self.slug])
    class Meta:
        verbose_name = "стихотворение"
        verbose_name_plural = "Все стихи"
        
class CommentActivated(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class Comment(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.PROTECT, related_name='comments', verbose_name='Стихотворение')
    name = models.CharField(max_length=255, verbose_name='Комментатор')
    ip = models.CharField("IP адрес", max_length=30)
    sess = models.TextField(verbose_name='Сессия', blank=True)
    telegram = models.CharField(max_length=255, verbose_name='Телеграм', blank=True)
    email = models.EmailField(verbose_name='Еmail', blank=True)
    body = models.TextField(verbose_name='Текст')
    created = models.DateField(verbose_name='Дата создания', default=date.today)
    active = models.BooleanField(default=False, verbose_name='Активность')
    objects = models.Manager()
    activeted = CommentActivated()
    

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return f'Комментарий от {self.name}'