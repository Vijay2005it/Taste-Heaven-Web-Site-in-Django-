from django import forms
from .models import CustomUser,FoodItem

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','email','password','user_type']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password  = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if password != confirm_password:
            raise forms.ValidationError("Password Mismatchd")
        
        if CustomUser.objects.filter(username = username).exists():
            raise forms.ValidationError('User Already Exists')

        if CustomUser.objects.filter(email = email).exists():
            raise forms.ValidationError('Email Already Exists')

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name',max_length=150)
    password = forms.CharField(label='Pasword',widget=forms.PasswordInput)


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control shadow-sm rounded'}),
            'description': forms.Textarea(attrs={'class': 'form-control shadow-sm rounded', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control shadow-sm rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control shadow-sm rounded'}),
        }
