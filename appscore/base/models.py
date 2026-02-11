from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de categoria")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Product(models.Model):

    name = models.CharField(max_length=100,verbose_name="Nombre de producto",unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Categoria")
    description = models.TextField( null=True,blank=True, verbose_name="Descripcion")

    def tojson(self):
        #item ={'id':self.id, 'name':self.name} #para pocos campos
        item = model_to_dict(self)
        return item

    class Meta:
         db_table = 'product'
         verbose_name = "Producto"
         verbose_name_plural = "Productos"
         ordering = ('name',)

    def __str__(self):
        return self.name

class ProductSupplier(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    price = models.DecimalField(max_digits=10, decimal_places=4)

