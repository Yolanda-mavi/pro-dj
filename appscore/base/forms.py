from django.db.models.fields import DecimalField
from django.forms import ModelForm
from django import forms
from django.forms.widgets import Textarea, TextInput, NumberInput
from django.views.generic import CreateView
from appscore.base.models import Product, Category,Bom,ProductUom,Country,Sector,FractionMx,FractionHtsus,FractionUsExp,FractionUs,Partner
#cambio pruebas11
#tambien existe un video 27 donde agrega propiedades por medio de una libreria tipo wigget que se instala (tweaks)

def comun_layout(form,layout):
    result = []
    for row in layout:
        cols=12 //len(row)
        result.append([
            {
                'field':form[field],
                'col':cols
            }
            for field in row
        ])
    return result

def customfield2_layout(form,layout):
    ##only cols pair
    result = []
    for row in layout:
        cols = int( len(row)/2)
        numero = 0
        cols_list = []
        for l in range( cols):
            cols_list.append(  {'field1': form[row[numero]], 'field2': form[row[numero+1]]}  )
            numero = numero + 2
            print("entro")
        result.append( cols_list )
    print(result)
    return result

class ProductForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        #para propiedades en comun
        for form in self.visible_fields():
            if form.name not in ['fraction_mx','country','sector','fraction_htsus','fraction_us','fraction_us_exp','category']:
                 form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            if form.widget_type == 'number':
                form.field.widget.attrs['step'] = '0.01'
                form.field.widget.attrs['style'] = '-moz-appearance: textfield; text-align: end;'
            if form.name in ['cost_tot','cost_av','cost','uc_or_stot','uc_nor_stot']:
                form.field.disabled = True

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            #para pocos capos se puede perzonalizar asi los campos
            'name': TextInput(attrs={
                'placeholder':"Ingresar nombre",
            }),
            'description': Textarea(attrs={
            'placeholder': "Ingresar descripción en espanol",
            'rows': 2,
            'cols': 50
            } ),
            'description_us': Textarea(attrs={
            'placeholder': "Ingresar descripción en ingles",
            'rows': 2,
            'cols': 50
            }),
            # 'cost_tot': forms.TextInput(attrs={
            #     'class': 'form-control text-end'
            # })


            # 'fraction_mx': forms.Select(attrs={'class': 'form-select'}),
            # 'fraction_htsus': forms.Select(attrs={'class': 'form-select'})

            # 'cost': NumberInput(attrs={
            #     'class': 'form-control',
            #     'step': '0.01',
            #     'style': '-moz-appearance: textfield;'
            # }),
            # 'cost_av': NumberInput(attrs={
            #     'class': 'form-control',
            #     'step': '0.01',
            #     'style': '-moz-appearance: textfield;'
            # })
        }

    #se me paso agregar el save

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <5:
            #raise  form.ValidationError("ingresar nombre")
            self.add_error('name',"Mayor a 5 ")
        # if cleaned.get('type') != 'F': PARA VACIAR CAMPOS OCULTOS
        #     cleaned['extra_field'] = None

        return cleaned

class CategoryForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True



    class Meta:
        model = Category
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"ingresar nombre",
            })
        }
    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <5:
            self.add_error('name',"El nombre es muy corto")
        return cleaned

class BomForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(BomForm, self).__init__(*args, **kwargs)
        #para porpiedades en comun
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Bom
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
                'placeholder':"ingresar nombre",
            })
        }

    #se me paso agregar el save

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <5:
            self.add_error('name',"no es muy long")
        return cleaned

class ProductUomForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(ProductUomForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            if form.widget_type == 'number':
                form.field.widget.attrs['step'] = '0.01'
                form.field.widget.attrs['style'] = '-moz-appearance: textfield; text-align: end;'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductUom
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class CountryForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Country
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class SectorForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Sector
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class FractionMxForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(FractionMxForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = FractionMx
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class FractionHtsusForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(FractionHtsusForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = FractionHtsus
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class FractionUsExpForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(FractionUsExpForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = FractionUsExp
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class FractionUsForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(FractionUsForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = FractionUs
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
            'placeholder':"Ingresar nombre",
            })
        }

class PartnerForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        #para porpiedades en comun
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Partner
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            'name': TextInput(attrs={
                'placeholder':"ingresar nombre",
            })
        }

    #se me paso agregar el save

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <5:
            self.add_error('name',"no es muy long")
        return cleaned

class ImportForm(forms.Form):


    type_list = [
        ('FractionMx', 'Fracciones Arancelaria Mexicana'),
        ('Product', 'Productos'),
        ('Category', 'Categorias'),
        ('ProductUom', 'Unidades de medida'),
        ('Country', 'Países'),
        ('Sector', 'Sectores'),
        ('FractionHtsus', 'Fracciones HTSUS'),
        ('FractionUs', 'Fracciones de usa'),
        ('FractionUsExp', 'Fracciones de usa para exportación'),
        ('Partner', 'Contactos'),
    ]
    model_name = forms.ChoiceField(initial='FractionMx',  choices=type_list)
    file_data = forms.FileField()


    def __init__(self,*args,**kwargs):
        super(ImportForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['model_name'].widget.attrs['autofocus'] = True

