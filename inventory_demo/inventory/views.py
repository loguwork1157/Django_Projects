import logging
from django.core.paginator import Paginator
from django.core.cache import cache

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
    # Session: Track visits to this page
    visit_count = request.session.get('visit_count', 0) + 1
    request.session['visit_count'] = visit_count

    # Caching: Try to get products from cache first
    products = cache.get('all_products')
    if not products:
        products = Product.objects.all()
        # Cache the queryset for 15 minutes
        cache.set('all_products', products, 60 * 15)

    # Pagination: Show 5 products per page
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    logger.info("Product list viewed by %s (Visit count: %d)", 
                request.user if request.user.is_authenticated else 'anonymous', 
                visit_count)
    
    return render(request, 'inventory/product_list.html', {
        'page_obj': page_obj,
        'visit_count': visit_count
    })


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
            logger.info("testing.... loggged in Successfully: %s", user.username)
            messages.success(request, "Welcome, your account was created.")
            return redirect('product_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    """Custom login view to handle user login."""
    from django.contrib.auth.forms import AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            logger.info("Testing User logged in: %s", user.username)
            messages.success(request, "You have been logged in.")
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/login.html', {'form': form})

# Custom logout view
def logout_view(request):
    """Log out the user and redirect to product list with a message."""
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('product_list')

def set_session_name(request):
    if request.method == 'POST':
        custom_name = request.POST.get('custom_name')
        if custom_name:
            request.session['custom_name'] = custom_name
            messages.success(request, f"Session name updated to {custom_name}")
        else:
            # clear it if empty
            if 'custom_name' in request.session:
                del request.session['custom_name']
                messages.success(request, "Session name cleared")
    return redirect('product_list')
