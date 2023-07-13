from . import views
from django.urls import path, include

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemsView.as_view()), 
    path('categories', views.CategoryView.as_view()), 
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()), 
    path('cart/orders', views.OrderView.as_view()),  
    path('cart/menu-items', views.CartItemView.as_view()), 
    path('groups/manager/users', views.ManagerView.as_view()), 
]