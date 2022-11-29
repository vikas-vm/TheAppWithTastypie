from django.db import models
from enum import Enum
from merchant.models import DiscountType
from authentication.models import User
# Create your models here.


class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, choices=[(
        tag, tag.value) for tag in Gender], null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customers'


class CustomerAddress(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer_addresses'


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey("merchant.Item", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'carts'


class PaymentMethod(Enum):
    CASH = 'Cash'
    CARD = 'Card'
    NETBANKING = 'NetBanking'
    UPIWALLET = 'UPIWallet'


class PaymentStatus(Enum):
    PENDING = 'Pending'
    SUCCESS = 'Success'
    FAILED = 'Failed'


class OrderStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    DELIVERED = 'Delivered'


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(
        "customer.CustomerAddress", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    total = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50, choices=[(
        tag, tag.value) for tag in PaymentMethod], default=PaymentMethod.CASH)
    payment_status = models.CharField(max_length=50, choices=[(
        tag, tag.value) for tag in PaymentStatus], default=PaymentStatus.PENDING)
    status = models.CharField(max_length=50, choices=[(
        tag, tag.value) for tag in OrderStatus], default=OrderStatus.PENDING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'orders'


class OrderItemStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    DELIVERED = 'Delivered'


class OrderItem(models.Model):
    order = models.ForeignKey("customer.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("merchant.Item", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    discount_type = models.CharField(
        max_length=50, choices=[(tag, tag.value) for tag in DiscountType], null=True, blank=True)
    amount_after_discount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[(
        tag, tag.value) for tag in OrderItemStatus], default=OrderItemStatus.PENDING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'order_items'
