from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

from .forms import ProductSearchForm, SinupForm , UpdateUserForm ,UpdatePasswordForm,UpdatUserInfo
from .models import Product,Category,Profile

from payments.forms import ShippingForm
from payments.models import ShippingAddress,Order,OrderItem


def botstrab(request):
    return render(request,"botstrab.html",{})



def update_info(request):
    if request.user.is_authenticated:
        # اگر پروفایل وجود نداشت، آن را برای این کاربر می‌سازد
        current_user, created = Profile.objects.get_or_create(user=request.user)
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        
        form = UpdatUserInfo(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if request.method == "POST" and (form.is_valid() or shipping_form.is_valid()):
            form.save()
            shipping_form.save()
            messages.success(request, "اطلاعات کاربر شما با موفقیت به روز رسانی شد.")
            return redirect("home")
            
        return render(request, 'update_info.html', {'form': form,'shipping_form':shipping_form})
    else:
        messages.error(request, "شما باید وارد شوید تا اطلاعات خود را به روز رسانی کنید.")
        return redirect("login")


def arif(request):
    shop =Product.objects.all()
    return render(request,"index.html",{'products':shop})



def About(request):
    return render(request,"about.html",{"about":About})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)

            current_user = Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)  # تبدیل رشته JSON به دیکشنری
                # اگر سبد خرید ذخیره شده وجود دارد، آن را به سبد خرید فعلی اضافه کنید
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

                # request.session['session_key'] = eval(saved_cart)  # تبدیل رشته به دیکشنری


            messages.success(request,('با موفقیت وارید شدید'))
            return redirect("home")
        else:
            messages.success(request,("مشکل در لاگین وجود دارد"))
            return redirect('login')
    return render(request,"login.html")



def logout_user(request):
    logout(request)
    messages.success(request,("شما موافقانه از سستم خارج شدید"))
    return redirect("home")



def sinup_user(request):
    form = SinupForm()
    if request.method == 'POST':
        # اطلاعا که کاربر پر کرده بریز داخل فورم
        form = SinupForm(request.POST)
        if form.is_valid():
            # اگر فورم مشکل نداشت بیا فورم را سیف کن
            form.save()
            # هر وقت کاربر ثبت مام می کند باید لاگین نمایم
            # پسورد و یوزر نیم را از این فور برمیدارم
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password1)
            # حالا باید لاگین نمایم
            login(request,user)
            messages.success(request,'اکانت سما ساخته شد')
            return redirect("home")
        else:
            messages.success(request,"مشکل در ثبت نام وحود دارد")
            return redirect("sinup")
    else:
        return render(request,'sinup.html',{'form':form})
   

def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def category(request, cat):
    cat = cat.replace("-", " ")
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'category': category,
            'products': products,
        })
    except Category.DoesNotExist:
        messages.success(request, "دسته بندی وجود ندارد")
        return redirect('home')


def cat_product(request):
    all_cat=Category.objects.all()
    return render(request,'cat_product.html',{'all_cat':all_cat})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(request.POST or None, instance=current_user)

        
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "اطلاعات شما با موفقیت به روز رسانی شد.")
            return redirect("home")
        return render(request, 'update_user.html', {'form': form})
    else:
        messages.success(request, "شما باید وارد شوید تا اطلاعات خود را به روز رسانی کنید.")
        return redirect("login")



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "رمز عبور شما با موفقیت به روز رسانی شد.")
                login(request, current_user)  # Re-authenticate the user after password change
                return redirect("home")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "شما باید وارد شوید تا رمز عبور خود را به روز رسانی کنید.")
        return redirect("home")

def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        return render(request, 'search.html', {'searched': searched, 'products': products})
        if not searched:
            messages.success(request, "لطفاً یک عبارت جستجو وارد کنید.")
            return render(request, 'search.html', {})

    return render(request, 'search.html', {})




def user_order(request):
    if request.user.is_authenticated:
        # حالا میخاهم صفارشات را بگیریم 
        delivered_ordered = Order.objects.filter(user = request.user ,status='Deliverd')
        other_orders = Order.objects.filter(user = request.user).exclude(status='Deliverd')
        context ={
            'delivered':delivered_ordered,
            'other':other_orders
        }
        return render(request,'order.html',context)
    else:
        messages.success(request,'دست رسی به این صفحه تا زمانیکی ثتب نکنید  امکان ندارد')
        return redirect('home')



def order_detail(request,pk):
    #حالا باید در این جا همان سفارش راپیدا نمایم
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        context ={

            'order':order,
            'items':items
        }
        return render(request,'order_detail.html',context)



    else:
        messages.success(request,'دست رسی به این صفحه تا زمانیکی ثتب نکنید  امکان ندارد')
        return redirect('home')



