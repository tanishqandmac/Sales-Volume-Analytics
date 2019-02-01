from shopify_auth.models import AbstractShopUser
from django.db import models

class AuthAppShopUser(AbstractShopUser):
    pass

class Users(models.Model):
    sno = models.AutoField(primary_key = True)
    domainName = models.CharField(max_length = 100, unique = True)
    flag = models.IntegerField(default = -1)
    utc_offset = models.CharField(max_length = 10, default = '+0000')
    def __str__(self):
        return (str(self.domainName))

class ProductsDatabase(models.Model):
    sno = models.ForeignKey(UserDatabase, on_delete=models.CASCADE)
    sku = models.IntegerField(default = 0)
    productName = models.CharField(max_length = 300)
    quantity = models.IntegerField(default = 0)
    vendor = models.CharField(max_length = 300, default = " - ")
    createdAt = models.DateTimeField()
