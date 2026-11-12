
from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.arif,name="home"),
    path('about/',views.About,name="about"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('sinup/',views.sinup_user,name="sinup"),
    path('update_user/',views.update_user,name='update_user'),
    path('update_password/',views.update_password,name='update_password'),
    path('update_info/',views.update_info,name='update_info'),
    path('product/<int:pk>/',views.product,name="product"),
    path('category/<str:cat>/', views.category, name='category'),
    path('botstrab/',views.botstrab,name='botstrab'),
    path('catagory/',views.cat_product,name='cat_product'),
    path('search/', views.search, name='search'),
    path('orders/', views.user_order, name='user_order'),
    path('order_detail/<int:pk>', views.order_detail, name='order_detail'),

    
]
