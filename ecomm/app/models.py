
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    joined_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    address = models.CharField(max_length=200 ,null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.id}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200 ,null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    mobile = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.full_name
    
CATEGORY_CHOICES=(
    ('TL',"Textile"),
    ('PT',"Painting"),
    ('PC',"Pottery&Cwramics"),
    ('SC',"Scluptures&Carving"),
    ('HL',"Handlooms"),
    ('MC',"MetalCrafts"),
    ('WE',"Weaving"),
)

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)
    

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveBigIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "CartProduct: " + str(self.id)
    

ORDER_STATUS = (
    ("Order Processing" , "Order Processing"),
    ("On the way" , "on the way"),
    ("Order Received" , "Order Received"),
    ("Order Completed" , "Order Completed"),
    ("Order Canceled" , "Order Canceled"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True ,blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50 ,choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: "+ str(self.id)
    
class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.customer.full_name} -> {self.product.title}"
