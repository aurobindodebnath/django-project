from .models import Solution
from django import forms

class SolutionForm(forms.ModelForm):

	class Meta:
		model= Solution
		fields= ('image', 'description')