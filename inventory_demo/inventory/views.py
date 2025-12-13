import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages

from .models import Product
from .forms import ProductForm, SignupForm

logger = logging.getLogger('inventory')

# Show all products
def product_list(request):
    # Existing product list view remains unchanged
    products = Product.objects.all()
    logger.info("Product list viewed by %s", request.user if request.user.is_authenticated else 'anonymous')
    return render(request, 'inventory/product_list.html', {'products': products})


# Add new product using manual HTML form (login required)
@login_required
def product_create(request):
    if request.method == 'POST':
        post_form = ProductForm(request.POST)
        if post_form.is_valid():
            product = post_form.save()
            logger.info("Product created by %s: id=%s name=%s", request.user.username, product.id, product.name)
            messages.success(request, "Product created successfully.")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})


# Edit an existing product (login required)
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.quantity = request.POST.get('quantity')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        logger.info("Product updated by %s: id=%s name=%s", request.user.username, product.id, product.name)
        messages.success(request, "Product updated successfully.")
        return redirect('product_list')

    form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})


# Delete a product (login required)
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        logger.info("Product deleted by %s: id=%s name=%s", request.user.username, product.id, product.name)
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_list')

    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


# Signup view (creates user and logs them in)
def signup(request):
    """Create a new user account and log them in."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_logged = auth_login(request, user)
            if user_logged is None:
                logger.info("Logged in Successfully: %s", user.username)
            messages.success(request, "Welcome, your account was created.")
            return redirect('product_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

# Custom logout view
def logout_view(request):
    """Log out the user and redirect to product list with a message."""
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('product_list')