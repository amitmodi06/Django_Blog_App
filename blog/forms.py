from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email_from = forms.EmailField(label="Email")
    email_to = forms.EmailField(label="To")
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()