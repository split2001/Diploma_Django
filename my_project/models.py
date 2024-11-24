from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    age = models.IntegerField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe')

    def __str__(self):
        return self.title
