from django.contrib.auth.models import AbstractUser
from django.db import models

# python manage.py makemigrations
# python manage.py migrate

# https://docs.djangoproject.com/en/4.1/topics/db/models/
# https://docs.djangoproject.com/en/4.1/topics/db/queries/
# https://docs.djangoproject.com/en/4.1/ref/models/instances/

# python manage.py shell
# from auctions.models import *
# Bids.objects.filter(wanted_product=5).order_by('-bid')[0].buyer.id

class User(AbstractUser):
    pass
    

class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    price= models.IntegerField()

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    buyer=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    wanted_product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    bid= models.IntegerField()

    def __str__(self):
        return f"{self.bid} - {self.buyer}"



    