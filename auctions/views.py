from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Product, Bids
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.models import Max

# python manage.py runserver
# https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django

# @login_required(login_url='login')
def index(request):
    return render(request, "auctions/index.html", {
        "productos": Product.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#formulario para crear nuevo prodructo
class nuevo_producto(forms.Form):
    titulo = forms.CharField(label="Product name", max_length=128, required=True)
    descripcion = forms.CharField(label="Description", max_length=640, required=True)
    precio = forms.IntegerField(label="Starting bid",  required=True)

# crear nuevo producto
def crear(request):
    if request.method=="POST":
        formulario1 = nuevo_producto(request.POST)
        
        if formulario1.is_valid():
            #informacion del formulario
            titulo = formulario1.cleaned_data["titulo"]
            descripcion = formulario1.cleaned_data["descripcion"]
            precio = formulario1.cleaned_data["precio"]

            usuario=request.user
   
            #guardar nuevo producto y redireccionarte a index
            nuevo= Product.objects.create(title=titulo, description= descripcion,author= usuario, price= precio)
            nuevo.save()
            return HttpResponseRedirect(reverse("index"))

    #inicio de la funcion crear, me lleva la pagina crear
    return render(request, "auctions/crear_producto.html", {
        "form": nuevo_producto(),
    })       

#formulario para crear nuevo prodructo
class nueva_oferta(forms.Form):
    oferta = forms.IntegerField(label="Place your bid", required=True) 

def ver(request, producto_id):
    producto = Product.objects.get(id=producto_id)
    precio =producto.price
    usuario=request.user

    # fintrando comprador con la oferta mas alta
    if Bids.objects.filter(wanted_product=producto):
        mayor_precio=Bids.objects.filter(wanted_product=producto).order_by("-bid")[:1].get().bid
        mayor_ofertador_id= Bids.objects.filter(wanted_product=producto).order_by('-bid')[0].buyer.id
        mayor_ofertador=User.objects.get(id=mayor_ofertador_id)
    else:
        mayor_precio=0
        mayor_ofertador= "No bids yet"

    # si se presiona el boton sumit y se envia la informacion del formulario, sucede estO:
    if request.method=="POST":
        formulario1 = nueva_oferta(request.POST)

        if formulario1.is_valid():
            #informacion del formulario
            oferta = formulario1.cleaned_data["oferta"]
                  
            # guardar la oferta si es valida
            if oferta >= precio and oferta > mayor_precio:
                
                nuevo= Bids.objects.create(buyer= usuario, wanted_product=producto, bid= oferta)
                nuevo.save()

                # Un reverse con url dinamico:
                return HttpResponseRedirect(reverse('ver', kwargs={'producto_id': producto_id}))
                
            
            # si la oferta no es lo suficientemente alta
            else:
                return render(request, "auctions/producto.html", {
                    "form": nueva_oferta(),
                    "producto": producto,
                    "mensaje1": "Bids must be higher than the starting price and the actual highest bid",
                    "precio": precio,
                    "mayor_precio": mayor_precio,
                    "ofertas": Bids.objects.all().order_by("-bid"),
                    "mayor_ofertador" : mayor_ofertador,
                    "usuario": usuario,
                    }) 
    
    # las ofertas estan ordenadas del mayor al menor gracias al .order_by
    return render(request, "auctions/producto.html", {
        "form": nueva_oferta(),
        "producto": producto,
        "precio": precio,
        "mayor_precio": mayor_precio,
        "ofertas": Bids.objects.all().order_by("-bid"), 
        "mayor_ofertador" : mayor_ofertador,
        "usuario": usuario,
        }) 