import django.forms as forms

from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ("is_active", "user", "status")


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    for field_name, field in self.fields.items():
    #        if field_name == 'price':
    #            # хотел сделать скрытым цену, но передумал
    #            #field.widget = forms.HiddenInput()
    #            print(field_name)
    #            print(field)
    #            print("____________________")
