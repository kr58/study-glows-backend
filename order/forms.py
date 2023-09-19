from django import forms

from order.models import (
    ORDER_STATUS,
    Order
)


class OrderForm(forms.ModelForm):
    choices = (('', '---'), ) + ORDER_STATUS
    status = forms.ChoiceField(choices=choices, required=False)

    class Meta:
        models = Order
        fields = '__all__'
