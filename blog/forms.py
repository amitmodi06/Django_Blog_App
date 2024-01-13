from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email_from = forms.EmailField(label="Email")
    email_to = forms.EmailField(label="To")
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)