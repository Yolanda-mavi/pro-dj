from django.db.models.fields import DecimalField
from django.forms import ModelForm
from django import forms
from django.forms.widgets import Textarea, TextInput, NumberInput
from django.views.generic import CreateView
from appscore.base.models import Product, Category,Bom,ProductUom,Country,Sector,FractionMx,FractionHtsus,FractionUsExp,FractionUs
#cambio pruebas11
#tambien existe un video 27 donde agrega propiedades por medio de una libreria tipo wigget que se instala (tweaks)
class ProductForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        #para propiedades en comun
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            if form.widget_type == 'number':
                form.field.widget.attrs['step'] = '0.01'
                form.field.widget.attrs['style'] = '-moz-appearance: textfield;'

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__' #puedes seleccionar campos o hacer una exclusion
        widgets = {
            #para pocos capos se puede perzonalizar asi los campos
            'name': TextInput(attrs={
                'placeholder':"ingresar nombre",
            }),
            'description': Textarea(attrs={
            'placeholder': "Ingresar descripción en espanol",
            'rows': 2,
            'cols': 100
            } ),
            'description_us': Textarea(attrs={
            'placeholder': "Ingresar descripción en ingles",
            'rows': 2,
            'cols': 100
            }),
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
            self.add_error('name',"no es muy long")
        print(cleaned)
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

class ImportForm(forms.Form):


    type_list = [
        ('FractionMx', 'Fracciones Arancelaria Mexicana'),
        ('Product', 'Productos'),
    ]
    model_name = forms.ChoiceField(initial='FractionMx',  choices=type_list)
    file_data = forms.FileField()


    def __init__(self,*args,**kwargs):
        super(ImportForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['model_name'].widget.attrs['autofocus'] = True

