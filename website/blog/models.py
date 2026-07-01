import jalali_date
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name




class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    reading_time = models.PositiveIntegerField(default=0 , verbose_name= "زمان مطالعه")
    view_counts = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name= "posts",null=True,blank=True,)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Ticket(models.Model):
    message = models.TextField(verbose_name=" بيام")
    name = models.CharField(max_length=250, verbose_name=" نام")
    email = models.EmailField(verbose_name=" ايميل ")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(max_length=250, verbose_name=" موضوع")

    class Meta:
        ordering = ['-phone']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "comments", verbose_name= "نویسنده" )
    name = models.CharField(max_length=250,verbose_name='نام')
    body = models.TextField(verbose_name= "متن کامنت")
    active = models.BooleanField(default=False,verbose_name= "وضعیت")
    created = models.TimeField(auto_now=True, verbose_name= "تاریخ ایجاد")
    publish = models.TimeField(auto_now=True, verbose_name= "انتشار")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f"{self.name} : {self.post}"

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


