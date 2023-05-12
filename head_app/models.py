from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

SONGS = (
  ('S', 'Stairway to Heaven'),
  ('H', 'Hotel California'),
  ('K', 'Kashmir'),
)

# Create your models here.
class Musician(models.Model):
  name=models.CharField(max_length=50)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('musicians_detail', kwargs={'pk': self.id})

class Guitar(models.Model):
  name = models.CharField(max_length=100)
  brand = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  year = models.IntegerField()
  musicians = models.ManyToManyField(Musician)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'guitar_id': self.id})

  def performed_today(self):
    return self.performing_set.filter(date=date.today()).count() >= len(SONGS)

class Performing(models.Model):
  date = models.DateField('Performing Date')
  song = models.CharField(
    max_length=1,
    choices=SONGS,
    default=SONGS[0][0]
  )
  # Create a guitar_id FK
  guitar = models.ForeignKey(
    Guitar,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"{self.get_song_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  cat = models.ForeignKey(Guitar, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for guitar_id: {self.guitar_id} @{self.url}"