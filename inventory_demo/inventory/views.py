from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

# Show all products
def product_list(request):
    products = Product.objects.all()
    return render(
        request, 'inventory/product_list.html', 
        {'products': products}
    )

# Add new product using manual HTML form
def product_create(request):
    if request.method == 'POST':
        post_form = ProductForm(request.POST)
        if post_form.is_valid():
            post_form.save()

        return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

# Edit an existing product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.quantity = request.POST.get('quantity')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        return redirect('product_list')

    if product:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})


# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'inventory/product_confirm_delete.html', {'product': product})
