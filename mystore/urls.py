from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product, name='product'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add-user', views.add_user, name='add-user'),
    path('remove-user/<str:_username>/', views.remove_user, name='remove-user'),
    path('update-cart/', views.update_cart, name='update-cart'),
    path('remove-from-cart/<int:product_id>', views.remove_from_cart, name='remove-from-cart'),
    path('categories/<str:category>', views.categories, name='categories'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order', views.place_order, name='place-order'),
    path('cancel-order/<int:id>/', views.cancel_order, name='cancel-order'),
    path('orders/', views.orders, name='orders'),
    path('user/', views.user, name='user'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
]