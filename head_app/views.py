import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Guitar, Performing, Musician, Photo
from .forms import PerformingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def guitars_index(request):
  guitars = Guitar.objects.filter(user=request.user)
  return render(request, 'guitars/index.html', {
    'guitars': guitars
  })

@login_required
def guitars_detail(request, guitar_id):
  guitar = Guitar.objects.get(id=guitar_id)
  id_list = guitar.musicians.all().values_list('id')
  guitars_not_performed_by_musician = Musician.objects.exclude(id__in=id_list)
  performing_form = PerformingForm()
  return render(request, 'guitars/detail.html', {
    'guitar': guitar, 'performing_form': performing_form,
    'musicians': guitars_not_performed_by_musician
  })

class GuitarCreate(LoginRequiredMixin, CreateView):
  model = Guitar
  fields = ['name', 'brand', 'description', 'year']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GuitarUpdate(UpdateView):
  model = Guitar
  fields = ['name', 'brand', 'description', 'year']

class GuitarDelete(DeleteView):
  model = Guitar
  success_url = '/guitars'

@login_required
def add_performing(request, guitar_id):
  form = PerformingForm(request.POST)
  if form.is_valid():
    new_performing = form.save(commit=False)
    new_performing.guitar_id = guitar_id
    new_performing.save()
  return redirect('detail', guitar_id=guitar_id)  

class MusicianList(LoginRequiredMixin, ListView):
  model = Musician

class MusicianDetail(LoginRequiredMixin, DetailView):
  model = Musician

class MusicianCreate(LoginRequiredMixin, CreateView):
  model = Musician
  fields = '__all__'

class MusicianUpdate(LoginRequiredMixin, UpdateView):
  model = Musician
  fields = ['name', 'color']

class MusicianDelete(LoginRequiredMixin, DeleteView):
  model = Musician
  success_url = '/musicians'

@login_required
def assoc_musician(request, guitar_id, musician_id):
  Guitar.objects.get(id=guitar_id).musicians.add(musician_id)
  return redirect('detail', guitar_id=guitar_id)

@login_required
def unassoc_musician(request, guitar_id, musician_id):
  Guitar.objects.get(id=guitar_id).musicians.remove(musician_id)
  return redirect('detail', guitar_id=guitar_id)

@login_required
def add_photo(request, guitar_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, guitar_id=guitar_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', caguitar_id=guitar_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)