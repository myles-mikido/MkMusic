from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre','cover','audio_file']



class SongBulkUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')