from django import forms
from core.models import User


#=====================================================
#================== Partner Form ====================
#=====================================================
class PartnerForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'
		widgets = {
			'english_name': forms.TextInput(attrs={'name':'english_name', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'English Name', 'required': 'True'}),
			'arabic_name': forms.TextInput(attrs={'name':'arabic_name', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'Arabic Name', 'required': 'True'}),
			'extension': forms.TextInput(attrs={'name':'extension', 'class': 'form-control', 'id': 'inputName', 'placeholder': '@aramco.com', 'required': 'True'}),
			'email': forms.TextInput(attrs={'name':'email', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'username@gmail.com', 'required': 'True'}),
			'photo': forms.FileInput(attrs={'name':'photo', 'id':"input-file-to-destroy", 'class':"dropify", 'data-max-file-size':"2M", 'data-max-height':"2000", 'required':'True'}),
			'phone': forms.TextInput(attrs={'name':'phone', 'class': 'form-control', 'id': 'inputName', 'placeholder': '0500000000', 'required': 'True'}),
			}


class UpdatePartnerForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'
		widgets = {
			'english_name': forms.TextInput(attrs={'name':'english_name', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'English Name', 'required': 'True'}),
			'arabic_name': forms.TextInput(attrs={'name':'arabic_name', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'Arabic Name', 'required': 'True'}),
			'extension': forms.TextInput(attrs={'name':'extension', 'class': 'form-control', 'id': 'inputName', 'placeholder': '@aramco.com', 'disabled':"True"}),
			'email': forms.TextInput(attrs={'name':'email', 'class': 'form-control', 'id': 'inputName', 'placeholder': 'username@gmail.com', 'disabled':"True"}),
			'photo': forms.FileInput(attrs={'name':'photo', 'id':"input-file-to-destroy", 'class':"dropify", 'data-max-file-size':"2M", 'data-max-height':"2000", 'required':'True'}),
			'phone': forms.TextInput(attrs={'name':'phone', 'class': 'form-control', 'id': 'inputName', 'placeholder': '0500000000', 'disabled':"True"}),
			}
#=====================================================
#=====================================================
#=====================================================