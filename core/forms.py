from django import forms
from core.models import User


#=====================================================
#================== Partner Form ====================
#=====================================================
class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'
		widgets = {
			'english_name': forms.TextInput(attrs={'name':'english_name', 'class': 'form-control border', 'id': 'inputName', 'placeholder': 'English Name', 'required': 'True'}),
			'arabic_name': forms.TextInput(attrs={'name':'arabic_name', 'class': 'form-control border text-right', 'id': 'inputName', 'placeholder': 'Arabic Name', 'required': 'True'}),
			}
#=====================================================
#=====================================================
#=====================================================