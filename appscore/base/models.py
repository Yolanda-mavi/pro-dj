from django.db import models
from django.forms import model_to_dict
from django.conf import settings

from core.models import AuditModel

class Category(AuditModel):


    name = models.CharField(max_length=200, verbose_name="Nombre de categoria",unique=True)
    #category = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True, verbose_name="Categoria")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[ (True,'Si'),(False,'No')])

    def __str__(self):
        # if not self.category:
        #     return self.name
        # full_name = "%s /  %s" % (self.category.name or '', self.name or '')
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def tojson(self):
        item = model_to_dict(self)
        return item

class ProductUom(AuditModel):

    name = models.CharField(max_length=200, verbose_name="Nombre",unique=True)
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_uom'
        verbose_name = 'Unidades de medida'
        verbose_name_plural = 'Unidades de medida'

    def tojson(self):
        item = model_to_dict(self)
        return item

class Country(AuditModel):
    code = models.CharField(max_length=15, verbose_name="Código", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
    def __str__(self):
        # full_name = "[%s] %s" % (self.code or '', self.name or '')
        # return full_name
        return self.name

    class Meta:
        db_table = 'country'
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def tojson(self):
        item = model_to_dict(self)
        return item

class Sector(AuditModel):
    code = models.CharField(max_length=15, verbose_name="Código", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        # full_name = "[%s] %s" % (self.code or '', self.name or '')
        # return full_name
        return self.name

    class Meta:
        db_table = 'sector'
        verbose_name = 'Sector autorizado'
        verbose_name_plural = 'Sectores autorizados'

    def tojson(self):
        item = model_to_dict(self)
        return item

class FractionMx(AuditModel):
    code = models.CharField(max_length=15, verbose_name="Código", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        # full_name = "[%s] %s" % (self.code or '', self.name or '')
        # return full_name
        return self.name

    class Meta:
        db_table = 'fraction_mx'
        verbose_name = 'Fracción Arancelaria Mexicana'
        verbose_name_plural = 'Fracciones Arancelarias Mexicana'

    def tojson(self):
        item = model_to_dict(self)
        return item

class FractionHtsus(AuditModel):
    code = models.CharField(max_length=15, verbose_name="Código", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        # full_name = "[%s] %s" % (self.code or '', self.name or '')
        # return full_name
        return self.name

    class Meta:
        db_table = 'fraction_htsus'
        verbose_name = 'Fracción HTSUS'
        verbose_name_plural = 'Fracciones HTSUS'

    def tojson(self):
        item = model_to_dict(self)
        return item

class FractionUs(AuditModel):
    code = models.CharField(max_length=15, verbose_name="Código", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        #full_name = "[%s] %s" % (self.code or '', self.name or '')
        #return full_name
        return self.name

    class Meta:
        db_table = 'fraction_us'
        verbose_name = 'Fracción de usa'
        verbose_name_plural = 'Fracciones de usa'

    def tojson(self):
        item = model_to_dict(self)
        return item

class FractionUsExp(AuditModel):
    code = models.CharField(max_length=15, verbose_name="Código", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        #full_name = "[%s] %s" % (self.code or '', self.name or '')
        #return full_name
        return self.name

    class Meta:
        db_table = 'fraction_us_exp'
        verbose_name = 'Fracción de usa para exportación'
        verbose_name_plural = 'Fracciones de usa para exportación'

    def tojson(self):
        item = model_to_dict(self)
        return item

class Product(AuditModel):

    type_list =[
        ('M','Material'),
        ('F', 'Producto Terminado'),
        ('A', 'Activo'),
    ]
    status_list = [
        ('N', 'Nuevos'),
        ('U', 'Usados'),
        ('R', 'Reconstruidos'),
        ('RM', 'Remanufacturados'),
    ]

    name = models.CharField(max_length=100,verbose_name="Nombre")
    code = models.CharField(max_length=25,null=True, blank=True, verbose_name="Codigo",unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Categoria")
    description = models.TextField( null=True,blank=True, verbose_name="Descripción")
    description_us = models.TextField( null=True,blank=True, verbose_name="Descripción (Ing)")
    #active = models.BooleanField(default=True, verbose_name="Activo")#estado
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
    nafta = models.BooleanField(default=False, verbose_name="Nafta")
    #obsolete = models.BooleanField(default=False, verbose_name="Estado") pienso que no se ocupa
    type = models.CharField(default='M',max_length=1,choices=type_list ,verbose_name='Tipo')
    status = models.CharField(default='N', max_length=2, choices=status_list,verbose_name='Estado de la mercancía.')
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Sector")
    country = models.ForeignKey(Country, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Pais")
    fraction_mx = models.ForeignKey(FractionMx, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Fracción MX")
    fraction_htsus = models.ForeignKey(FractionHtsus,on_delete=models.PROTECT,null=True,blank=True, verbose_name="Fracción HTSUS")
    fraction_us = models.ForeignKey(FractionUs, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Fracción US")
    fraction_us_exp = models.ForeignKey(FractionUsExp,on_delete=models.PROTECT,null=True,blank=True, verbose_name="Fracción US exportación")
    weight_pack = models.FloatField(default=0.0, verbose_name="Peso de empaque (kg)")
    weight_mat = models.FloatField(default=0.0, verbose_name="Peso de material (kg)")
    weight = models.FloatField(default=0.0, verbose_name="Peso (kg)")
    #weight_lb = models.FloatField(default=0.0, verbose_name="Peso (lb)") deberia ser calculado / investigar
    fac_po = models.FloatField(default=0.0, verbose_name="Factor de compra")
    fac_po_uom = models.ForeignKey(ProductUom,on_delete=models.PROTECT,null=True,blank=True, verbose_name="Unidad de medida de factor de compra",related_name="+")
    fac_co = models.FloatField(default=0.0, verbose_name="Factor comercial")
    fac_co_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidad de medida de factor comercial")
    fac_rate = models.FloatField(default=0.0, verbose_name="Factor de tarifa en comercio exterior")
    fac_rate_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidad de medida de tarifa de comercio exterior",related_name="+")
    fac_bom = models.FloatField(default=0.0, verbose_name="Factor en bom")
    fac_bom_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidad de medida de bom",related_name="+")
    fac_rate_us = models.FloatField(default=0.0, verbose_name="Factor de tarifa us")
    fac_rate_us_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Unidad de medida de factor comercial",related_name="+")
    fac_so = models.FloatField(default=0.0, verbose_name="Factor de venta")
    fac_so_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Unidad de medida de venta",related_name="+")

    cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.0,verbose_name="Costo")
    cost_av = models.DecimalField(max_digits=10, decimal_places=4, default=0.0,verbose_name="Valor agregado")
    #cost_total = models.DecimalField(max_digits=10, decimal_places=4, default=0.0,verbose_name="Costo total") deberia ser calculado

    cd_mat_or = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Materia prima originario")
    cd_mat_nor = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Materia prima no originario")
    cd_pack_or = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Empaques originario")
    cd_pack_nor = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Empaques no originario")
    #cd_or_stot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Sub-Total originario") debe calcular
    #cd_nor_stot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Sub-Total no originario") debe calcular
    #cd_tot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Costo Unitario") debe calcular

    cd_av_ind = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado indirectos")
    cd_av_dir = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado directos")
    cd_av_nat = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado nacionales")
    #cd_av_stot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado Sub-Total") valor calculado
    #cd_av_tot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Costo Unitario + Valor agregado") calor calculado







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

class Partner(AuditModel):
    name = models.CharField(max_length=200, verbose_name="Nombre")


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'partner'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def tojson(self):
        item = model_to_dict(self)
        return item

class ProductSupplier(AuditModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    price = models.DecimalField(max_digits=10, decimal_places=4,default=0.0,verbose_name="Precio")
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT,null=True,blank=True,  verbose_name="Proveedor")

    class Meta:
         db_table = 'product_supplier'

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

    def __str__(self):
        return self.product_id.name