from django import forms
from submit.models import CodeSubmission
from problems.models import Problem

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),
    ("cpp", "C++"),
]

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Language'})
    )
    code = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control code-editor',
            'rows': 15,
            'autocomplete': 'on',
            'placeholder': 'Enter your code here...'
        })
    )
    input_data = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Optional input data'
        })
    )

    class Meta:
        model = CodeSubmission
        fields = ['problem', 'language', 'code', 'input_data']
        widgets = {
            'problem': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Problem'}),
        }
