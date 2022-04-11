from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def get_default_key():
    return Blog.objects.get(id=1)


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# class Blog(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     updated = models.DateTimeField(auto_now=True)
#     blog_image = models.URLField(max_length=250,
#                                  default='https://images.pexels.com/photos/6071881/pexels-photo-6071881.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default=get_default_key)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#
#     class Meta:
#         ordering = ['-timestamp']
#         verbose_name_plural = 'Blogs'
#
#     def __str__(self):
#         return self.title
