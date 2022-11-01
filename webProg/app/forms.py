from django import forms
from .models import Book, User, Order, CartItem


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'
