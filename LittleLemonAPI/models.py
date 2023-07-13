from django.db import models
from django.contrib.auth.models import Group 
from django.contrib.auth import get_user_model
from django.db.models import F, Sum

# Create your models here.
class Category(models.Model): 
    title = models.CharField(max_length=255) 

    def __str__(self) -> str:
        return self.title 

class MenuItem(models.Model): 
    title = models.CharField(max_length=255) 
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    featured = models.BooleanField() 
    
    def __str__(self) -> str:
        return self.title

class ManagerManager(models.Manager): 
    def get_queryset(self): 
        manager_group = Group.objects.get(name='Manager')
        return super().get_queryset().filter(groups=manager_group) 
    
class Manager(get_user_model()): 
    class Meta: 
        proxy = True 
    
    objects = ManagerManager() 

class CustomerManager(models.Manager): 
    def get_queryset(self): 
        customer_group = Group.objects.get(name='Customer')
        return super().get_queryset().filter(groups=customer_group) 
    
class Customer(get_user_model()): 
    class Meta: 
        proxy = True 
    
    objects = CustomerManager()  

class DeliveryCrewManager(models.Manager): 
    def get_queryset(self): 
        delivery_crew_group = Group.objects.get(name="Delivery Crew") 
        return super().get_queryset().filter(groups=delivery_crew_group) 

class DeliveryCrew(get_user_model()): 
    class Meta: 
        proxy = True 
    
    objects = DeliveryCrewManager() 

class Order(models.Model): 
    delivery_crew = models.ForeignKey(DeliveryCrew, on_delete=models.DO_NOTHING, related_name="order_delivered", null=True, db_constraint=False) 
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="order_placed", null=True, db_constraint=False)  
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateField(db_index=True)
    delivered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return 'menu-items'
    
class Cart(models.Model): 
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) 
    items = models.ManyToManyField(MenuItem, through='CartItem')  
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return str(self.customer.username)
    
    def calculate_total(self):
        total_price = self.orderitem_set.aggregate(total_price=Sum(F('item__price') * F('quantity')))['total_price']
        self.total = total_price
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 

    def __str__(self) -> str:
        return 'menu-items'