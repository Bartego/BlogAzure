from django import forms

from images.models import Image


class UploadForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['title', 'file']
        labels = {
            'file': "Image",
        }

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)