from django.db import models
from django.contrib.auth.models import User


# class MLModel(models.Model):
#     file = models.FileField(upload_to='models')
#     accuracy = models.FloatField()
#     train_date = models.DateField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class News(models.Model):
    #user= models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    name= models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    text = models.TextField()	
    label = models.BooleanField(default=True, verbose_name="True")
    category = models.ForeignKey(Category, on_delete= models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null = True)
    def __str__(self):
        return f'{self.title},{self.label}'
	
class CategoryNews(models.Model):
    news= models.ForeignKey(News,on_delete=models.CASCADE)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)

# class Feedback(models.Model):
#     name = models.CharField(max_length=500)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     label = models.BooleanField(default=True)
#     categorys = models.Ch
    
    













