from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2", "placeholder": "Product name"}),
            "description": forms.Textarea(attrs={"class": "w-full border rounded px-3 py-2", "rows": 4, "placeholder": "Details..."}),
            "price": forms.NumberInput(attrs={"class": "w-full border rounded px-3 py-2", "step": "0.01", "min": "0"}),
            "category": forms.Select(attrs={"class": "w-full border rounded px-3 py-2"}),
            "image": forms.ClearableFileInput(attrs={"class": "w-full"}),
        }

    def clean_category(self):
        c = self.cleaned_data["category"]
        valid = [c[0] for c in Category.choices]
        if c not in valid:
            raise forms.ValidationError("Invalid category.")
        return c
