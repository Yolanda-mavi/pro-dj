from django.db import models
from django.forms import model_to_dict
from appscore.inventory.models import Product
from core.models import AuditModel

class Bom(AuditModel):

    name = models.CharField(max_length=100,verbose_name="Nombre de lista",unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def tojson(self):
        item = model_to_dict(self)

        return item

    class Meta:
         db_table = 'bom'
         verbose_name = "Lista de materiales"
         verbose_name_plural = "Listas de materiales"
         ordering = ('name',)

    def __str__(self):
        return self.name

class Bomline(AuditModel):

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    bom = models.ForeignKey(Bom, on_delete=models.CASCADE, verbose_name="Bom")


    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
         db_table = 'bom_line'
         verbose_name = "Lista de materiales"
         verbose_name_plural = "Listas de materiales"
         # ordering = ('name',)

    # def __str__(self):
    #     return self.product_id.name