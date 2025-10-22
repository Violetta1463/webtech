from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'message', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Сообщение (до 500 символов)'}),
        }


    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Имя слишком короткое')
        return name

    def clean_message(self):
        msg = self.cleaned_data['message'].strip()
        if 'http://' in msg or 'https://' in msg:
            raise forms.ValidationError('Ссылки запрещены')
        return msg
