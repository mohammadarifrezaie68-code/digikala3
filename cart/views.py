from itertools import product

from django.shortcuts import render,get_object_or_404


# mee
from .cart import Cart
from shops.models import Product
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_product()
    quantities = cart.get_quants()
    total = cart.get_total()
    return render(request,'cart_summary.html',{'cart_products':cart_products,'quantities':quantities,'total':total})




def cart_add(request):
    cart =Cart(request)

    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product,id=product_id)
        cart.add(product=product , quantity=product_qty)

        cart_quantity =len(cart)
        respons = JsonResponse(
            {'qty': cart_quantity,
             'product_name':product.name
             })
        return respons




def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)
        respons = JsonResponse({'product name': product_id})
        return respons  
    
def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product,id=product_id)
        cart.update(product=product_id , quantity=product_qty)

        cart_quantity =len(cart)

        respons = JsonResponse(
            {'qty': cart_quantity,
             'product_name':product.name
             })
        return respons



    