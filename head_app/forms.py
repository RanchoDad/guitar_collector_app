from django.forms import ModelForm
from .models import Performing

class PerformingForm(ModelForm):
  class Meta:
    model = Performing
    fields = ['date', 'song']

