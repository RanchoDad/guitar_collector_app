from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Guitar
from .forms import PerformingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def guitars_index(request):
  guitars = Guitar.objects.all()
  return render(request, 'guitars/index.html', {
    'guitars': guitars
  })

def guitars_detail(request, guitar_id):
  guitar = Guitar.objects.get(id=guitar_id)
  performing_form = PerformingForm()
  return render(request, 'guitars/detail.html', {
    'guitar': guitar, 'performing_form': performing_form
  })

class GuitarCreate(CreateView):
  model = Guitar
  fields = '__all__'

class GuitarUpdate(UpdateView):
  model = Guitar
  fields = ['name', 'brand', 'description', 'year']

class GuitarDelete(DeleteView):
  model = Guitar
  success_url = '/guitars'

def add_performing(request, guitar_id):
  form = PerformingForm(request.POST)
  if form.is_valid():
    new_performing = form.save(commit=False)
    new_performing.guitar_id = guitar_id
    new_performing.save()
  return redirect('detail', guitar_id=guitar_id)  