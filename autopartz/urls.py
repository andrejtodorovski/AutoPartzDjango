from django.conf.urls.static import static
from django.urls import path

from hw5 import settings
from .views import login_view, register_view, parts_view, \
    part_details, add_to_cart, shopping_cart, home, logout_view, profile_view, my_orders_view, delivery_info, \
    successful_order, order_details, remove_from_cart, admin_orders, add_part, change_order_status

urlpatterns = [
                  path('', home, name='home'),
                  path('login/', login_view, name='login'),
                  path('register/', register_view, name='register'),
                  path('parts/', parts_view, name='parts'),
                  path('parts/<int:pk>/', part_details, name='part_details'),
                  path('parts/<int:pk>/add-to-cart/', add_to_cart, name='add_to_cart'),
                  path('shopping-cart/', shopping_cart, name='shopping_cart'),
                  path('logout/', logout_view, name='logout'),
                  path('profile/', profile_view, name='profile'),
                  path('my-orders/', my_orders_view, name='my_orders'),
                  path('delivery-info', delivery_info, name='delivery_info'),
                  path('successful-order', successful_order, name='successful_order'),
                  path('order/<int:pk>/', order_details, name='order_details'),
                  path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
                  path('admin-orders', admin_orders, name='admin_orders'),
                  path('add-part', add_part, name='add_part'),
                  path('change-order-status/<int:pk>/', change_order_status, name='change_order_status'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
