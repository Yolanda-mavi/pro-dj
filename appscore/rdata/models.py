from django.db import models
from django.forms import model_to_dict
from core.models import AuditModel
from appscore.base.models import Country,State

class Partner(AuditModel):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    first_surname = models.CharField(max_length=100, verbose_name="Primer apellido",null=True, blank=True)
    second_surname = models.CharField(max_length=100, verbose_name="Segundo apellido",null=True, blank=True)
    curp = models.CharField(max_length=18, verbose_name="CURP",null=True, blank=True)
    rfc = models.CharField(max_length=13, verbose_name="RFC",null=True, blank=True)
    irs = models.CharField(max_length=15, verbose_name="I.R.S.",null=True, blank=True)#no se que es
    alr = models.CharField(max_length=15, verbose_name="ALR",null=True, blank=True)#no se que es
    patent = models.CharField(max_length=15, verbose_name="Patente",null=True, blank=True)#no se que es
    phone = models.CharField(max_length=30, verbose_name="Telefono",null=True, blank=True)
    mobile = models.CharField(max_length=30, verbose_name="Mobile",null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name="E-mail",null=True, blank=True)
    website = models.CharField(max_length=50, verbose_name="Website",null=True, blank=True)

    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Pais")
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Estado")
    city = models.CharField(max_length=100, verbose_name="Ciudad",null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name="Direccion",null=True, blank=True)
    address_num = models.CharField(max_length=20, verbose_name="Numero",null=True, blank=True)
    address_num_int = models.CharField(max_length=20, verbose_name="Numero interior",null=True, blank=True)
    zip = models.CharField(max_length=20, verbose_name="C.P.",null=True, blank=True)
    po_box = models.CharField(max_length=20, verbose_name="P.O. box",null=True, blank=True)

    #agencia coder broker file and brocker importer
    #transportista creo que esto es en otra tabla por viaje hay que preguntar caat broker care scac fast ctpat

    #Choferes
    #informacion medica y direccion
    card = models.CharField(max_length=50, verbose_name="Gafete",null=True, blank=True)
    #company_trans = models.ForeignKey(Partner, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Compania transportista")
    gender = models.CharField(default='1', max_length=1, verbose_name="Genero", choices=[('1', 'Hombre'), ('2', 'Mujer')])
    birthdate = models.DateField(verbose_name="Fecha de nacimiento",null=True, blank=True)
    registration_dt = models.DateField(verbose_name="Fecha de alta",null=True, blank=True)
    off_dt = models.DateField(verbose_name="Fecha de baja",null=True, blank=True)
    license_exp_dt = models.DateField(verbose_name="Vigencia de licencia",null=True, blank=True)
    card_exp_dt = models.DateField(verbose_name="Vigencia de gafette",null=True, blank=True)
    card_fast_exp_dt = models.DateField(verbose_name="Vigencia tarjeta fast",null=True, blank=True)

    legal_rep = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,related_name='legal_representative_for',limit_choices_to={'is_repr': True},verbose_name="Representante legal" )


    # lr_name = models.CharField(max_length=100, verbose_name="Nombre de representante")
    # lr_first_surn = models.CharField(max_length=100, verbose_name="Primer apellido de representante")
    # lr_second_surn = models.CharField(max_length=100, verbose_name="Segundo apellido de representante")
    # lr_rfc = models.CharField(max_length=13, verbose_name="RFC de representante")

    # customer = models.BooleanField(default=True, verbose_name="Es cliente", choices=[(True, 'Si'), (False, 'No')])
    # supplier = models.BooleanField(default=True, verbose_name="Es proveedor", choices=[(True, 'Si'), (False, 'No')])
    # repr = models.BooleanField(default=False, verbose_name="Es representante legal", choices=[(True, 'Si'), (False, 'No')])
    # driver = models.BooleanField(default=False, verbose_name="Es chofer", choices=[(True, 'Si'), (False, 'No')])
    # agency = models.BooleanField(default=False, verbose_name="Es agencia", choices=[(True, 'Si'), (False, 'No')])
    # active = models.BooleanField(default=False, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])
    partner = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='company_partners',limit_choices_to={'is_company': True}, verbose_name="Compañia")

    is_customer = models.BooleanField(default=True, verbose_name="Es cliente")
    is_supplier = models.BooleanField(default=True, verbose_name="Es proveedor")
    is_repr = models.BooleanField(default=False, verbose_name="Es representante legal")
    is_driver = models.BooleanField(default=False, verbose_name="Es chofer")
    is_agency = models.BooleanField(default=False, verbose_name="Es agencia")
    is_company = models.BooleanField(default=False, verbose_name="Es compañia")
    active = models.BooleanField(default=False, verbose_name="Activo", choices=[(True, 'Si'), (False, 'No')])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'partner'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def tojson(self):
        item = model_to_dict(self)
        return item
