from django import forms
from django.forms import ModelForm
from main.models import Products

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ["name", "price", "description", "category", "thumbnail", "is_featured", "stock"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6CABDD]"
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6CABDD]"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6CABDD]"
            }),
            "category": forms.TextInput(attrs={
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6CABDD]"
            }),
            "thumbnail": forms.URLInput(attrs={
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6CABDD]"
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 text-[#6CABDD] border-gray-300 rounded focus:ring-[#6CABDD]"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6CABDD]"
            }),
        }
