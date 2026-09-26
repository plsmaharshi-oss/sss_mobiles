from django import forms

from .models import Mobile


class MobileForm(forms.ModelForm):
    """Validated input for creating and updating inventory items."""

    class Meta:
        model = Mobile
        fields = ('brand', 'model_name', 'ram', 'storage', 'price', 'condition', 'description', 'image')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price
