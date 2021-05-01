from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime



# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    body = models.TextField()

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self): 
        return reverse('post_detail', args=[str(self.id)])
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('post_detail')