from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product

@login_required
def products(request):
    query = Q()
    if 'name' in request.GET:
        query &= Q(name__icontains=request.GET['name'])
    if 'item_code' in request.GET:
        query &= Q(item_code__icontains=request.GET['item_code'])
    if 'HS' in request.GET and request.GET['HS'] == 'on':
        query &= Q(HS=True)
    if 'AS' in request.GET and request.GET['AS'] == 'on':
        query &= Q(AS=True)
    if 'RC' in request.GET and request.GET['RC'] == 'on':
        query &= Q(RC=True)
    if 'PC' in request.GET and request.GET['PC'] == 'on':
        query &= Q(PC=True)
    if 'default' in request.GET and request.GET['default'] == 'on':
        query &= Q(default=True)
    if 'sleva' in request.GET and request.GET['sleva'] == 'on':
        query &= Q(sleva=True)

    products = Product.objects.filter(query)

    return render(request, 'products.html', {'products': products})

@login_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.item_code = request.POST['item_code']
        product.description = request.POST['description']
        product.sale_price = request.POST['sale_price']
        product.purchase_price = request.POST['purchase_price']
        product.product_type = request.POST['product_type']
        product.DPH = request.POST['DPH']
        product.url = request.POST['url']
        product.HS = 'HS' in request.POST
        product.AS = 'AS' in request.POST
        product.RC = 'RC' in request.POST
        product.PC = 'PC' in request.POST
        product.default = 'default' in request.POST
        product.sleva = 'sleva' in request.POST

        product.save()
        return redirect('products')

    return render(request, 'edit_product.html', {'product': product})
