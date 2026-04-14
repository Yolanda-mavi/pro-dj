from django.db import models
from django.forms import model_to_dict
from django.conf import settings
from django.db.models import F,DecimalField
from core.models import AuditModel

# class Category(AuditModel):
#
#
#     name = models.CharField(max_length=200, verbose_name="Nombre de categoria",unique=True)
#     #category = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True, verbose_name="Categoria")
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[ (True,'Si'),(False,'No')])
#
#     def __str__(self):
#         # if not self.category:
#         #     return self.name
#         # full_name = "%s /  %s" % (self.category.name or '', self.name or '')
#         return self.name
#
#     class Meta:
#         db_table = 'category'
#         verbose_name = 'Categoria'
#         verbose_name_plural = 'Categorias'
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item
#
# class ProductUom(AuditModel):
#
#     name = models.CharField(max_length=200, verbose_name="Nombre",unique=True)
#     factor = models.FloatField(default=0.0, verbose_name="Factor")
#     base = models.BooleanField(default=True, verbose_name="Base", choices=[(True, 'Si'), (False, 'No')])
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'product_uom'
#         verbose_name = 'Unidades de medida'
#         verbose_name_plural = 'Unidades de medida'
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item

class Country(AuditModel):
    code_m3 = models.CharField(max_length=2, verbose_name="Clave SAAI M3",blank=True,null=True)
    code_fiii = models.CharField(max_length=4, verbose_name="Clave SAAI FIII", unique=True,blank=True,null=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
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

class State(AuditModel):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
    def __str__(self):
        # full_name = "[%s] %s" % (self.code or '', self.name or '')
        # return full_name
        return self.name

    class Meta:
        db_table = 'state'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def tojson(self):
        item = model_to_dict(self)
        return item

class Sector(AuditModel):
    code = models.CharField(max_length=2, verbose_name="Código", unique=True)
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

# class FractionMx(AuditModel):
#     code = models.CharField(max_length=15, verbose_name="Código", unique=True)
#     name = models.TextField(verbose_name="Nombre")
#     cal_imp = models.CharField(max_length=100, verbose_name="Importación",blank=True,null=True)
#     cal_exp = models.CharField(max_length=100, verbose_name="Exportación",blank=True,null=True)
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#
#     def __str__(self):
#         # full_name = "[%s] %s" % (self.code or '', self.name or '')
#         # return full_name
#         return self.code
#
#     class Meta:
#         db_table = 'fraction_mx'
#         verbose_name = 'Fracción Arancelaria Mexicana'
#         verbose_name_plural = 'Fracciones Arancelarias Mexicana'
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item
#
# class FractionHtsus(AuditModel):
#     code = models.CharField(max_length=15, verbose_name="Código")
#     nico = models.CharField(max_length=2, verbose_name="NICO", blank=True, null=True)
#     name = models.TextField( verbose_name="Nombre")
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#     def __str__(self):
#         full_name = "%s %s" % (self.code or '', self.nico or '')
#         return full_name
#         #return self.code
#
#     class Meta:
#         db_table = 'fraction_htsus'
#         verbose_name = 'Fracción HTSUS'
#         verbose_name_plural = 'Fracciones HTSUS'
#         unique_together = ('code', 'nico')
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item
#
# class FractionUs(AuditModel):
#     code = models.CharField(max_length=15, verbose_name="Código", unique=True)
#     name = models.CharField(max_length=200, verbose_name="Nombre")
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#     def __str__(self):
#         #full_name = "[%s] %s" % (self.code or '', self.name or '')
#         #return full_name
#         return self.code
#
#     class Meta:
#         db_table = 'fraction_us'
#         verbose_name = 'Fracción de usa'
#         verbose_name_plural = 'Fracciones de usa'
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item
#
# class FractionUsExp(AuditModel):
#     code = models.CharField(max_length=15, verbose_name="Código", unique=True)
#     name = models.CharField(max_length=200, verbose_name="Nombre")
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#     def __str__(self):
#         #full_name = "[%s] %s" % (self.code or '', self.name or '')
#         #return full_name
#         return self.code
#
#     class Meta:
#         db_table = 'fraction_us_exp'
#         verbose_name = 'Fracción de usa para exportación'
#         verbose_name_plural = 'Fracciones de usa para exportación'
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item

# class Product(AuditModel):
#
#     type_list =[
#         ('M','Material'),
#         ('F', 'Producto Terminado'),
#         ('A', 'Activo'),
#     ]
#     status_list = [
#         ('N', 'Nuevos'),
#         ('U', 'Usados'),
#         ('R', 'Reconstruidos'),
#         ('RM', 'Remanufacturados'),
#     ]
#
#     name = models.CharField(max_length=100,verbose_name="Nombre")
#     code = models.CharField(max_length=25,null=True, blank=True, verbose_name="Codigo",unique=True)
#     category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Categoria")
#     description = models.TextField( null=True,blank=True, verbose_name="Descripción")
#     description_us = models.TextField( null=True,blank=True, verbose_name="Descripción (Ing)")
#     #active = models.BooleanField(default=True, verbose_name="Activo")#estado
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#     nafta = models.BooleanField(default=False, verbose_name="Nafta")
#     #obsolete = models.BooleanField(default=False, verbose_name="Estado") pienso que no se ocupa
#     type = models.CharField(default='M',max_length=1,choices=type_list ,verbose_name='Tipo')
#     status = models.CharField(default='N', max_length=2, choices=status_list,verbose_name='Estado de la mercancía')
#     sector = models.ForeignKey(Sector, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Sector")
#     country = models.ForeignKey(Country, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Pais")
#     fraction_mx = models.ForeignKey(FractionMx, on_delete=models.PROTECT,null=True,blank=True, verbose_name="Fracción MX")
#     fraction_htsus = models.ForeignKey(FractionHtsus,on_delete=models.PROTECT,null=True,blank=True, verbose_name="Fracción HTSUS")
#     fraction_us = models.ForeignKey(FractionUs, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Fracción US")
#     fraction_us_exp = models.ForeignKey(FractionUsExp,on_delete=models.PROTECT,null=True,blank=True, verbose_name="Fracción US exportación")
#     weight_pack = models.FloatField(default=0.0, verbose_name="Peso de empaque (kg)")
#     weight_mat = models.FloatField(default=0.0, verbose_name="Peso de material (kg)")
#     weight = models.FloatField(default=0.0, verbose_name="Peso (kg)")
#     #weight_lb = models.FloatField(default=0.0, verbose_name="Peso (lb)") deberia ser calculado / investigar
#     fac_po = models.FloatField(default=0.0, verbose_name="Factor de compra")
#     fac_po_uom = models.ForeignKey(ProductUom,on_delete=models.PROTECT,null=True,blank=True, verbose_name="Unidad de medida de factor de compra",related_name="+")
#     fac_co = models.FloatField(default=0.0, verbose_name="Factor comercial")
#     fac_co_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidad de medida de factor comercial")
#     fac_rate = models.FloatField(default=0.0, verbose_name="Factor tarifa de com. exterior", help_text="Factor de tarifa de comercio exterior" )
#     fac_rate_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidad de medida de tarifa de comercio exterior",related_name="+")
#     fac_bom = models.FloatField(default=0.0, verbose_name="Factor en bom")
#     fac_bom_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidad de medida de bom",related_name="+")
#     fac_rate_us = models.FloatField(default=0.0, verbose_name="Factor de tarifa us")
#     fac_rate_us_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Unidad de medida de factor comercial",related_name="+")
#     fac_so = models.FloatField(default=0.0, verbose_name="Factor de venta")
#     fac_so_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Unidad de medida de venta",related_name="+")
#
#     cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.0,  verbose_name="Costo unitario")
#     cost_av = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado")
#
#     uc_mat_or = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Materia prima originario")
#     uc_mat_nor = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Materia prima no originario")
#     uc_pack_or = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Empaques originario")
#     uc_pack_nor = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Empaques no originario")
#     uc_or_stot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0,  verbose_name="Sub-Total originario")
#     uc_nor_stot = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Sub-Total no originario")
#
#     cav_ind = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado indirectos")
#     cav_dir = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado directos")
#     cav_nat = models.DecimalField(max_digits=10, decimal_places=4, default=0.0, verbose_name="Valor agregado nacionales")
#     cost_tot = models.DecimalField(max_digits=10,decimal_places=4, default=0.0, verbose_name="costo total" )
#
#     def tojson(self):
#         #item ={'id':self.id, 'name':self.name} #para pocos campos
#         item = model_to_dict(self)
#         return item
#
#     class Meta:
#          db_table = 'product'
#          verbose_name = "Producto"
#          verbose_name_plural = "Productos"
#          ordering = ('name',)
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         self.uc_or_stot = (self.uc_mat_or or 0) + (self.uc_pack_or or 0)
#         self.uc_nor_stot = (self.uc_mat_nor or 0) + (self.uc_pack_nor or 0)
#         self.cost = (self.uc_mat_or or 0) + (self.uc_pack_or or 0) + (self.uc_mat_nor or 0) + (self.uc_pack_nor or 0)
#         self.cost_av = (self.cav_ind or 0) + (self.cav_dir or 0) + (self.cav_nat or 0)
#         self.cost_tot = (self.uc_mat_or or 0) + (self.uc_pack_or or 0) + (self.uc_mat_nor or 0) + (self.uc_pack_nor or 0) + (self.cav_ind or 0) + (self.cav_dir or 0) + (self.cav_nat or 0)
#         super().save(*args, **kwargs)

# class Partner(AuditModel):
#     name = models.CharField(max_length=200, verbose_name="Nombre")
#     first_surname = models.CharField(max_length=100, verbose_name="Primer apellido",null=True, blank=True)
#     second_surname = models.CharField(max_length=100, verbose_name="Segundo apellido",null=True, blank=True)
#     curp = models.CharField(max_length=18, verbose_name="CURP",null=True, blank=True)
#     rfc = models.CharField(max_length=13, verbose_name="RFC",null=True, blank=True)
#     irs = models.CharField(max_length=15, verbose_name="I.R.S.",null=True, blank=True)#no se que es
#     alr = models.CharField(max_length=15, verbose_name="ALR",null=True, blank=True)#no se que es
#     patent = models.CharField(max_length=15, verbose_name="Patente",null=True, blank=True)#no se que es
#     phone = models.CharField(max_length=30, verbose_name="Telefono",null=True, blank=True)
#     mobile = models.CharField(max_length=30, verbose_name="Mobile",null=True, blank=True)
#     email = models.CharField(max_length=50, verbose_name="E-mail",null=True, blank=True)
#     website = models.CharField(max_length=50, verbose_name="Website",null=True, blank=True)
#
#     country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Pais")
#     state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Estado")
#     city = models.CharField(max_length=100, verbose_name="Ciudad",null=True, blank=True)
#     address = models.CharField(max_length=100, verbose_name="Direccion",null=True, blank=True)
#     address_num = models.CharField(max_length=20, verbose_name="Numero",null=True, blank=True)
#     address_num_int = models.CharField(max_length=20, verbose_name="Numero interior",null=True, blank=True)
#     zip = models.CharField(max_length=20, verbose_name="C.P.",null=True, blank=True)
#     po_box = models.CharField(max_length=20, verbose_name="P.O. box",null=True, blank=True)
#
#     #agencia coder broker file and brocker importer
#     #transportista creo que esto es en otra tabla por viaje hay que preguntar caat broker care scac fast ctpat
#
#     #Choferes
#     #informacion medica y direccion
#     card = models.CharField(max_length=50, verbose_name="Gafete",null=True, blank=True)
#     #company_trans = models.ForeignKey(Partner, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Compania transportista")
#     gender = models.CharField(default='1', max_length=1, verbose_name="Genero", choices=[('1', 'Hombre'), ('2', 'Mujer')])
#     birthdate = models.DateField(verbose_name="Fecha de nacimiento",null=True, blank=True)
#     registration_dt = models.DateField(verbose_name="Fecha de alta",null=True, blank=True)
#     off_dt = models.DateField(verbose_name="Fecha de baja",null=True, blank=True)
#     license_exp_dt = models.DateField(verbose_name="Vigencia de licencia",null=True, blank=True)
#     card_exp_dt = models.DateField(verbose_name="Vigencia de gafette",null=True, blank=True)
#     card_fast_exp_dt = models.DateField(verbose_name="Vigencia tarjeta fast",null=True, blank=True)
#
#     legal_rep = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,related_name='legal_representative_for',limit_choices_to={'is_repr': True},verbose_name="Representante legal" )
#
#
#     # lr_name = models.CharField(max_length=100, verbose_name="Nombre de representante")
#     # lr_first_surn = models.CharField(max_length=100, verbose_name="Primer apellido de representante")
#     # lr_second_surn = models.CharField(max_length=100, verbose_name="Segundo apellido de representante")
#     # lr_rfc = models.CharField(max_length=13, verbose_name="RFC de representante")
#
#     # customer = models.BooleanField(default=True, verbose_name="Es cliente", choices=[(True, 'Si'), (False, 'No')])
#     # supplier = models.BooleanField(default=True, verbose_name="Es proveedor", choices=[(True, 'Si'), (False, 'No')])
#     # repr = models.BooleanField(default=False, verbose_name="Es representante legal", choices=[(True, 'Si'), (False, 'No')])
#     # driver = models.BooleanField(default=False, verbose_name="Es chofer", choices=[(True, 'Si'), (False, 'No')])
#     # agency = models.BooleanField(default=False, verbose_name="Es agencia", choices=[(True, 'Si'), (False, 'No')])
#     # active = models.BooleanField(default=False, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#     partner = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='company_partners',limit_choices_to={'is_company': True}, verbose_name="Compañia")
#
#     is_customer = models.BooleanField(default=True, verbose_name="Es cliente")
#     is_supplier = models.BooleanField(default=True, verbose_name="Es proveedor")
#     is_repr = models.BooleanField(default=False, verbose_name="Es representante legal")
#     is_driver = models.BooleanField(default=False, verbose_name="Es chofer")
#     is_agency = models.BooleanField(default=False, verbose_name="Es agencia")
#     is_company = models.BooleanField(default=False, verbose_name="Es compañia")
#     active = models.BooleanField(default=False, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'partner'
#         verbose_name = 'Contacto'
#         verbose_name_plural = 'Contactos'
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item

#
# class ProductSupplier(AuditModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
#     price = models.DecimalField(max_digits=10, decimal_places=4,default=0.0,verbose_name="Precio")
#     partner = models.ForeignKey(Partner, on_delete=models.PROTECT,null=True,blank=True,  verbose_name="Proveedor")
#
#     class Meta:
#          db_table = 'product_supplier'

#
# class Bom(AuditModel):
#
#     name = models.CharField(max_length=100,verbose_name="Nombre de lista",unique=True)
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
#     active = models.BooleanField(default=True, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
#
#     def tojson(self):
#         item = model_to_dict(self)
#
#         return item
#
#     class Meta:
#          db_table = 'bom'
#          verbose_name = "Lista de materiales"
#          verbose_name_plural = "Listas de materiales"
#          ordering = ('name',)
#
#     def __str__(self):
#         return self.name
#
# class Bomline(AuditModel):
#
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
#     quantity = models.PositiveIntegerField(verbose_name="Cantidad")
#     bom = models.ForeignKey(Bom, on_delete=models.CASCADE, verbose_name="Bom")
#
#
#     def tojson(self):
#         item = model_to_dict(self)
#         return item
#
#     class Meta:
#          db_table = 'bom_line'
#          verbose_name = "Lista de materiales"
#          verbose_name_plural = "Listas de materiales"
#          # ordering = ('name',)
#
#     # def __str__(self):
#     #     return self.product_id.name