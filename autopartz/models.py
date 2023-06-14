from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=100,
                                 choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric'),
                                          ('hybrid', 'Hybrid'), ('gas', 'Gas')])
    engine_displacement = models.IntegerField()
    horse_power = models.IntegerField()
    seats = models.IntegerField()
    doors = models.IntegerField()
    body_type = models.CharField(max_length=100,
                                 choices=[('sedan', 'Sedan'), ('hatchback', 'Hatchback'), ('coupe', 'Coupe'),
                                          ('convertible', 'Convertible'), ('suv', 'SUV'), ('minivan', 'Minivan'),
                                          ('pickup', 'Pickup')])

    def __str__(self):
        return self.brand + ' ' + self.car_model + ' ' + str(self.year) + ' ' + self.fuel_type + ' ' + str(
            self.engine_displacement) + 'cc ' + str(self.horse_power) + 'hp ' + self.body_type


class Part(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    available = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    compatible_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    def __str__(self):
        return self.part.name

    def subtotal(self):
        return self.part.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100,
                                    choices=([('In progress', 'In progress'), ('Delivered', 'Delivered')]))

    def __str__(self):
        return str(self.id)


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices=([('On Delivery', 'On Delivery'), ('Card', 'Card')]))

    def __str__(self):
        return self.full_name
