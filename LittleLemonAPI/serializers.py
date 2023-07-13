from rest_framework import serializers 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from .models import MenuItem, Category, Order, Cart, OrderItem, CartItem, Manager

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = ['id', 'title'] 
        
class MenuItemSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = MenuItem 
        fields = ['id', 'title', 'price', 'category', 'featured']

    def get_fields(self):
        fields = super().get_fields() 
        user = self.context['request'].user 

        if user.groups.filter(name="Manager").exists(): 
            for field_name in fields:  
                if field_name != 'featured': 
                    fields[field_name].read_only = True 
        elif user.groups.filter(name="Admin").exists(): 
            pass 
        else: 
            for field_name in fields:  
                fields[field_name].read_only = True
            
        return fields 

class OrderItemSerializer(serializers.ModelSerializer): 
    menu_item = MenuItemSerializer(many=False, read_only=True, source='item')
    class Meta: 
        model = OrderItem
        fields = ['menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer): 
    items = OrderItemSerializer(many=True, source='orderitem_set')
    class Meta: 
        model = Order 
        fields = ['id', 'customer_id', 'delivery_crew_id', 'delivered', 'items', 'total', 'date'] 

    def get_fields(self):
        fields = super().get_fields() 
        user = self.context['request'].user 

        if user.groups.filter(name="Manager").exists(): 
            for field_name in fields:  
                if field_name != 'delivery_crew_id': 
                    fields[field_name].read_only = True 
        elif user.groups.filter(name='Delivery Crew').exists():
            for field_name in fields:
                if field_name != 'delivered':
                    fields[field_name].read_only = True
        else: 
            for field_name in fields:  
                if field_name != 'date': 
                    fields[field_name].read_only = True 
            
        return fields 

class CartItemSerializer(serializers.ModelSerializer): 
    menu_item = MenuItemSerializer(many=False, source='item')
    class Meta: 
        model = CartItem
        fields = ['menu_item', 'quantity'] 

class CartSerializer(serializers.ModelSerializer): 
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')
    class Meta: 
        model = Cart 
        fields = ['customer_id', 'items', 'total'] 

class ManagerSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Manager 
        fields = ['id', 'username']

