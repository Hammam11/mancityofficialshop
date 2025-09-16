from django.forms import ModelForm
from main.models import Products

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ["name", "price", "description", "category", "thumbnail", "products_solds", "is_featured"]