from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('arif/', include('shops.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payments.urls')),
    
    # جایگزین تابع static برای کار کردن در حالت DEBUG=False
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
