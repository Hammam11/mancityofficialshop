from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductsForm
from main.models import Products
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        products_list = Products.objects.all()
    else:
        products_list = Products.objects.filter(user=request.user)

    context = {
        'npm': '2406401350',
        'name': request.user.username,
        'class': 'PBP B',
        'products_list': products_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)


@login_required(login_url='/login')
def create_products(request):
    form = ProductsForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        products_entry = form.save(commit=False)
        products_entry.user = request.user
        products_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_products.html", context)


@login_required(login_url='/login')
def show_products(request, id):
    products = get_object_or_404(Products, pk=id)
    context = {'products': products}
    return render(request, "products_detail.html", context)


@login_required(login_url='/login')
def purchase_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # gunakan method purchase di models.py
        if product.purchase(quantity):
            return redirect('main:show_main')
        else:
            return render(request, 'out_of_stock.html')


def show_xml(request):
    products_list = Products.objects.all()
    xml_data = serializers.serialize("xml", products_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    products_list = Products.objects.all()
    data = [
        {
            'id': products.id,
            'name': products.name,
            'price': products.price,
            'description': products.description,
            'category': products.category,
            'thumbnail': products.thumbnail,
            'products_solds': products.products_solds,
            "stock": products.stock,
            #'created_at': products.created_at.isoformat() if products.created_at else None,
            'is_featured': products.is_featured,
            'user_id': products.user_id,
        }
        for products in products_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, products_id):
    try:
        products_item = Products.objects.filter(pk=products_id)
        xml_data = serializers.serialize("xml", products_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Products.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, products_id):
    try:
        products = Products.objects.select_related('user').get(pk=products_id)
        data = {
            'id': str(products.id),
            'name': products.name,
            'description': products.description,
            'category': products.category,
            'thumbnail': products.thumbnail,
            'products_solds': products.products_solds,
            #'created_at': products.created_at.isoformat() if products.created_at else None,
            'is_featured': products.is_featured,
            'user_id': products.user_id,
            'user_username': products.user.username if products.user_id else None,
        }
        return JsonResponse(data)
    except Products.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('main:login')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Invalid username or password!')
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


@login_required(login_url='/login')
def delete_products(request, id):
    products = get_object_or_404(Products, pk=id)
    
    # hanya owner yang bisa hapus
    if products.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this product.")

    products.delete()
    return HttpResponseRedirect(reverse('main:show_main'))


@login_required(login_url='/login')
def edit_products(request, id):
    products = get_object_or_404(Products, pk=id)

    if products.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this product.")

    form = ProductsForm(request.POST or None, instance=products)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "edit_products.html", context)

@csrf_exempt
@require_POST
def add_products_entry_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    stock = request.POST.get("stock")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_products = Products(
        name=name, 
        price=price, 
        description=description,
        category=category,
        thumbnail=thumbnail,
        stock=stock,
        is_featured=is_featured,
        user=user
    )
    
    new_products.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def update_product_ajax(request, id):
    try:
        product = Products.objects.get(pk=id, user=request.user)  # pastiin yang edit itu pemiliknya
    except Products.DoesNotExist:
        return HttpResponse(b"NOT FOUND", status=404)

    product.name = strip_tags(request.POST.get("name"))
    product.price = request.POST.get("price")
    product.description = strip_tags(request.POST.get("description"))
    product.category = request.POST.get("category")
    product.thumbnail = request.POST.get("thumbnail")
    product.is_featured = request.POST.get("is_featured") == 'on'
    product.save()

    return HttpResponse(b"UPDATED", status=200)

@csrf_exempt
def login_ajax(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            response = JsonResponse({"success": True})
            # Tambah cookie last_login biar tampil di main page
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        return JsonResponse({"success": False, "message": "Invalid username or password"})
    return JsonResponse({"success": False, "message": "Invalid request"})

@csrf_exempt
def register_ajax(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return JsonResponse({"success": False, "message": "Passwords do not match"})
        if user.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already taken"})

        user = user.objects.create_user(username=username, password=password1)
        user.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid request"})

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def delete_product_ajax(request, id):
    try:
        product = Products.objects.get(pk=id, user=request.user)
        product.delete()
        return JsonResponse({"success": True, "message": "Product deleted"})
    except Products.DoesNotExist:
        return JsonResponse({"success": False, "message": "Product not found"}, status=404)
