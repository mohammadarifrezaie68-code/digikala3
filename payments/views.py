from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm
from django.contrib import messages 
from shops.models import Product, Profile
from django.contrib.auth.models import User


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def check_out(request):
    cart = Cart(request)
    cart_products = cart.get_product()
    quantities = cart.get_quants()
    total = cart.get_total()
    
    if request.user.is_authenticated:
        try:
            # استفاده از try-except برای جلوگیری از خطای DoesNotExist کاربر جدید
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm(request.POST or None)
            
        return render(request, 'payment/check_out.html', {'cart_products': cart_products, 'quantities': quantities, 'total': total, 'shipping_form': shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/check_out.html', {'cart_products': cart_products, 'quantities': quantities, 'total': total, 'shipping_form': shipping_form})


def confirm_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_product()
        quantities = cart.get_quants()
        total = cart.get_total()
        
        user_shipping = request.POST
        request.session['user_shipping'] = user_shipping
        # اجبار جنگو به ثبت و ذخیره سیشن برای کاربران مهمان
        request.session.modified = True

        # اصلاح مشکل اول: هر دو کاربر (عضو و مهمان) باید به صفحه confirm_order هدایت شوند
        if request.user.is_authenticated:
            return render(request, 'payment/confirm_order.html', {'cart_products': cart_products, 'quantities': quantities, 'total': total, 'shipping_info': user_shipping})
        else:
            # هدایت درست کاربر مهمان به صفحه تایید صورت‌حساب به جای check_out
            return render(request, 'payment/confirm_order.html', {'cart_products': cart_products, 'quantities': quantities, 'total': total, 'shipping_info': user_shipping})
    else:
        # تغییر سطح پیام از موفقیت به خطا برای دسترسی غیرمجاز
        messages.error(request, 'دسترسی به این صفحه امکان ندارد')
        return redirect('home')


def process_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_product()
        quantities = cart.get_quants()
        total = cart.get_total()
        
        user_shipping = request.session.get('user_shipping')
        if not user_shipping:
            messages.error(request, 'اطلاعات ارسال در سیشن یافت نشد. مجدداً تلاش کنید.')
            return redirect('home')
        
        full_name = user_shipping.get('shipping_full_name', '')
        email = user_shipping.get('shipping_email', '')
        address1 = user_shipping.get('shipping_address1', '')
        address2 = user_shipping.get('shipping_address2', '')
        city = user_shipping.get('shipping_city', '')
        state = user_shipping.get('shipping_state', '')
        zipcode = user_shipping.get('shipping_zipcode', '')
        country = user_shipping.get('shipping_country', '')
        
        full_address = f"{address1}\n{address2}\n{city}\n{state}\n{zipcode}\n{country}"
        
        # ۱. مرحله اول: ایجاد و ثبت سفارش کلی (Order) بر اساس وضعیت لاگین کاربر
        # اصلاح مشکل دوم: کدهای میانی حذف شدند تا بلاک if و else کاملاً به هم متصل بمانند
        if request.user.is_authenticated:
            new_order = Order(
                user=request.user,
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total
            )
        else:
            new_order = Order( 
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total
            )
        
        # ذخیره سفارش اصلی در دیتابیس
        new_order.save()
        
        # ۲. مرحله دوم: ثبت اقلام سبد خرید (OrderItem)
        for product in cart_products:
            prod = get_object_or_404(Product, id=product.id)
            
            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price

            for k, v in quantities.items():
                if int(k) == product.id:
                    new_item = OrderItem(
                        order=new_order,  
                        product=prod,
                        price=price,
                        quantity=v,
                    )
                    # اصلاح مشکل دوم: فعال‌سازی ثبت اتوماتیک کاربر روی تک‌تک اقلام سفارش در دیتابیس
                    if request.user.is_authenticated: 
                        new_item.user = request.user
                        
                    new_item.save()
                    
        # ۳. مرحله سوم: پاک کردن سبد خرید قدیمی و اطلاعات سیشن (انتقال کدهای جابجا شده به مکان درست و نهایی)
        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]

        if request.user.is_authenticated:
            cu = Profile.objects.filter(user__id=request.user.id)
            cu.update(old_cart="")
            
        if 'user_shipping' in request.session:
            del request.session['user_shipping']
        
        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return redirect('home')
        
    else:
        messages.error(request, 'دسترسی به این صفحه امکان‌پذیر نیست.')
        return redirect('home')
