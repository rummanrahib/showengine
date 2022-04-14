from platform import platform

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ShowList(models.Model):
    # ForeignKey Fields
    platform = models.ForeignKey(
        'StreamPlatform', on_delete=models.CASCADE, related_name='show_list')
    # ...

    title = models.CharField(max_length=100)
    plot = models.TextField()
    average_rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Show List'
        verbose_name_plural = 'Show Lists'

    def __str__(self):
        return self.title


class StreamPlatform(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    web = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stream Platform'
        verbose_name_plural = 'Stream Platforms'

    def __str__(self):
        return self.name


class Review(models.Model):
    # ForeignKey Fields
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    show_list = models.ForeignKey(
        'ShowList', on_delete=models.CASCADE, related_name='reviews')
    # ...

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.show_list.title} | {self.rating} | {self.author}'
