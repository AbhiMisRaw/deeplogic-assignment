
import os
from django.core.exceptions import ValidationError
from django import forms

class FileUploadForm(forms.Form):


    def validate_file_extension(value):
        
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
        print(ext)
        print("value :", value)
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension. Only PDF, PNG, JPG, JPEG files are allowed.')
        
    file_object = forms.FileField(required=True,label="Choose a file.",widget=forms.FileInput(attrs={
        'class':'form-control'
    }),   validators=[validate_file_extension])
