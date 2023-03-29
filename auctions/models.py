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

"""
---- Comandos para subir repositorio nuevo a github ---
git init
git remote add origin -link- // crea un repositorio nuevo en github y copia el link ahi
git status // see the status of your local files
git add * // add files
git commit -m "message" // Git map the changes
git push origin master // upload files

---- Guardar repositorio modificado ----
git add .
git commit -m "version2"
-  git commit -am "some message"  - // si solo se modificaron archivos los2 pasos anteriores se resumen en este
git push origin master

----crear nueva rama---
git branch // ver rama actual
git checkout -b <new branch name> // To make a new branch
git checkout <branch name>  // cambiarse a otra rama

"""


 
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



    