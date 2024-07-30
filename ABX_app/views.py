from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product, ProductType
from django.db.models import Q

def authenticate_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if authenticate_user(request, username, password):
            return redirect('main_page')
        else:
            return render(request, 'login.html', {'form': {'errors': True}})
    return render(request, 'login.html')

@login_required
def main_page(request):
    return render(request, 'main_page.html')

@login_required
def offers(request):
    return render(request, 'offers.html')

@login_required
def new_offer(request):
    return render(request, 'new_offer.html')

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
    product_types = ProductType.objects.all()

    return render(request, 'products.html', {'products': products, 'product_types': product_types})

@login_required
def get_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_data = {
        'id': product.id,
        'item_code': product.item_code,
        'name': product.name,
        'description': product.description,
        'url': product.url,
        'sale_price': product.sale_price,
        'purchase_price': product.purchase_price,
        'DPH': product.DPH,
        'HS': product.HS,
        'AS': product.AS,
        'RC': product.RC,
        'PC': product.PC,
        'default': product.default,
        'sleva': product.sleva,
        'product_type': product.product_type.id,
    }
    return JsonResponse(product_data)

@login_required
@csrf_exempt
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.item_code = request.POST['item_code']
        product.description = request.POST['description']
        product.url = request.POST['url']
        product.sale_price = request.POST['sale_price']
        product.purchase_price = request.POST['purchase_price']
        product.DPH = request.POST['DPH']
        product.HS = request.POST.get('HS', False) == 'on'
        product.AS = request.POST.get('AS', False) == 'on'
        product.RC = request.POST.get('RC', False) == 'on'
        product.PC = request.POST.get('PC', False) == 'on'
        product.default = request.POST.get('default', False) == 'on'
        product.sleva = request.POST.get('sleva', False) == 'on'
        product_type_id = request.POST['product_type']
        product.product_type = get_object_or_404(ProductType, id=product_type_id)
        product.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})
