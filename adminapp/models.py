from django.db import models


class MerchantModel(models.Model):
    id_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    username = models.EmailField(unique=True)
    contact = models.IntegerField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    product_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    merchant = models.ForeignKey(MerchantModel, on_delete=models.CASCADE)


class CustomerModel(models.Model):
    id_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    contact = models.IntegerField(unique=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)
