# from django import forms
# from .models import Order
# from django.utils.translation import gettext_lazy as _
#
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model=Order
#         fields=['firs_name','last_name','phone_number','address','orders_notes']
#         widgets={
#             'address':forms.Textarea(attrs={'rows':3,'style':'resize:none',}),
#             'orders_notes': forms.Textarea(attrs={
#                 'rows': 5,
#                 'style':'resize:none',
#                 'placeholder':_('if you have any notes please enter here otherwise leave it empty.')})
#         }
