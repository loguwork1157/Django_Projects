from django.db import models

# Create your models here.
class ProductPrices(models.Model):
    price = models.FloatField()

class ProductCategory(models.Model):
    category = models.CharField(max_length=40)

class Product(models.Model):
    name = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
