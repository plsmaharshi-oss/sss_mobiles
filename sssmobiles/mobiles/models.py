from django.db import models

class Mobile(models.Model):
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    ram = models.CharField(max_length=20)
    storage = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='mobiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"

# Create your models here.
