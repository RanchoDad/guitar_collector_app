from django.db import models
from django.urls import reverse

SONGS = (
  ('S', 'Stairway to Heaven'),
  ('H', 'Hotel California'),
  ('K', 'Kashmir'),
)

# Create your models here.
class Guitar(models.Model):
  name = models.CharField(max_length=100)
  brand = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  year = models.IntegerField()

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'guitar_id': self.id})

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
