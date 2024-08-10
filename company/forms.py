from django import forms
from core.models import User


#=====================================================
#================== Partners Form ====================
#=====================================================
class EmployeeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'
		widgets = {
			'english_name': forms.TextInput(attrs={'name':'english_name', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'English Name', 'required': 'True'}),
			'arabic_name': forms.TextInput(attrs={'name':'arabic_name', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'Arabic Name', 'required': 'True'}),
			'email': forms.TextInput(attrs={'name':'email', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'username@gmail.com', 'required': 'True'}),
			'phone': forms.TextInput(attrs={'name':'phone', 'class': 'form-control', 'id': 'inputName', 'placeholder': '0500000000', 'required': 'True'}),
			}
#=====================================================
#=====================================================
#=====================================================