from rest_framework import generics, filters
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .models import MenuItem, Category, Cart, Manager, CartItem, Order
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, ManagerSerializer, CartItemSerializer, OrderSerializer
from .permissions import IsManagerOrDeliveryCrewOrReadOnly, IsCustomer, IsAdminOrReadOnly, IsAdminOrReadOnly, IsAdmin, IsManagerOrReadOnly

# Create your views here.
class CategoryView(generics.ListCreateAPIView): 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter] 
    search_fields = ['title']
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price']  
    search_fields = ['title'] 
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly] 

class SingleMenuItemsView(generics.RetrieveUpdateAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer 
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

class OrderView(generics.ListCreateAPIView): 
    queryset = Order.objects.all() 
    serializer_class = OrderSerializer 
    permission_classes = [permissions.IsAuthenticated, IsManagerOrDeliveryCrewOrReadOnly]

    def get_queryset(self):
        user = self.request.user 
        return Order.objects.filter(delivery_crew=user) or Order.objects.filter(customer=user) 
    
    def create(self, request, *args, **kwargs): 
        date = request.data['date'] 
        customer = self.request.user 
        cart = Cart.objects.get(customer_id=customer.id) 
        
        order = Order.objects.create(customer=customer,  total=cart.total, date=date) 
        order.items.set(cart.items.all())
        order.save() 
        
        cart.items.clear() 
        cart.total = 0.00 
        cart.save() 

        return Response(data={'message': 'order placed'}, status=status.HTTP_201_CREATED)

class SingleOrderView(generics.RetrieveUpdateAPIView): 
    queryset = Order.objects.all() 
    serializer_class = OrderSerializer 
    permission_classes = [permissions.IsAuthenticated, IsManagerOrDeliveryCrewOrReadOnly] 

    def get_queryset(self):
        user = self.request.user 
        return Order.objects.filter(delivery_crew=user)

class CartView(generics.ListCreateAPIView): 
    queryset = Cart.objects.all() 
    serializer_class = CartSerializer 
    permission_classes = [permissions.IsAuthenticated, IsCustomer] 

    def get_queryset(self):
        user = self.request.user 
        return Order.objects.filter(customer=user)  
    
class CartItemView(generics.ListCreateAPIView): 
    queryset = CartItem.objects.all() 
    serializer_class = CartItemSerializer 
    permission_classes = [permissions.IsAuthenticated, IsCustomer] 

    def get_queryset(self):
        user = self.request.user 
        return CartItem.objects.filter(cart_id=user.id) 

class ManagerView(generics.ListCreateAPIView): 
    queryset = Manager.objects.all() 
    serializer_class = ManagerSerializer 
    permission_classes = [permissions.IsAuthenticated, IsAdmin] 

    def assgin_to_manager(self, request, *args, **kwargs):  
        user = User.objects.get(username=request.data['username'])
        group = Group.objects.get(name='Manager') 
        user.groups.add(group) 
        return Response(data={'message': 'user added to the manager group'}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        return self.assgin_to_manager(request, *args, **kwargs)

    
