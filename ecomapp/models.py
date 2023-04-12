from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager 
from django_resized import ResizedImageField


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200,null=True,blank=True)
    joined_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

 

class Category(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    # image=models.ImageField(upload_to='products')
    image=ResizedImageField(size=[500, 300],upload_to='products')
    marked_price=models.PositiveBigIntegerField()
    selling_price=models.PositiveBigIntegerField()
    description=models.TextField()
    warranty=models.CharField(max_length=300,null=True,blank=True)
    return_policy=models.CharField(max_length=300,null=True,blank=True)
    view_count=models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    total=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart'+ str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity=models.PositiveBigIntegerField()
    subtotal=models.PositiveIntegerField()

    def __str__(self):
        return 'Cart'+ str(self.id) + 'CartProduct:'+ str(self.id)

ORDER_STATUS=(
    ('Order Received','Order Received'),
    ('Order Processing','Order Processing'),
    ('On the way ','On the way '),
    ('Order Completed','Order Completed'),
    ('Order Cancelled','Order Cancelled')
)

METHOD=(
    ('Cash On Delivery','Cash On Delivery'),
    ('Esewa','Esewa')
)

class Order(models.Model):


    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    order_by=models.CharField(max_length=200)
    shipping_address=models.CharField(max_length=200)
    mobile=models.CharField(max_length=10)
    email=models.EmailField(null=True,blank=True)
    subtotal=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    total=models.PositiveIntegerField()
    order_status=models.CharField(max_length=50,choices=ORDER_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    payment_method=models.CharField(max_length=20,choices=METHOD,default='Cash On Delivery')
    payment_completed=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return 'Order'+ str(self.id)


  

    
      
