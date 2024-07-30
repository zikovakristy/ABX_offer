from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    item_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    url = models.URLField(default="")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    default = models.BooleanField(default=False)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    HS = models.BooleanField(default=False)
    AS = models.BooleanField(default=False)
    RC = models.BooleanField(default=False)
    PC = models.BooleanField(default=False)
    sleva = models.BooleanField(default=False)
    DPH = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    @property
    def price_with_DPH(self):
        return self.sale_price * (1 + self.DPH / 100)

    def __str__(self):
        return self.name
    
class RegionGroup(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(RegionGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Offer(models.Model):
    client = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_modified_user = models.ForeignKey(User, related_name='last_modified_offers', on_delete=models.CASCADE, null=True)
    created_by_user = models.ForeignKey(User, related_name='created_offers', on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Offer {self.id} for {self.client}"

class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

class OfferPDF(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='offers/')
