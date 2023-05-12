from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('guitars/', views.guitars_index, name='index'),
  path('guitars/<int:guitar_id>/', views.guitars_detail, name='detail'),
  path('guitars/create/', views.GuitarCreate.as_view(), name='guitars_create'),
  path('guitars/<int:pk>/update/', views.GuitarUpdate.as_view(), name='guitars_update'),
  path('guitars/<int:pk>/delete/', views.GuitarDelete.as_view(), name='guitars_delete'),
  path('guitars/<int:guitar_id>/add_performing/', views.add_performing, name='add_performing'),
  path('guitars/<int:guitar_id>/add_photo/', views.add_photo, name='add_photo'),
  path('guitars/<int:guitar_id>/assoc_musician/<int:musician_id>/', views.assoc_musician, name='assoc_musician'),
  path('guitars/<int:guitar_id>/unassoc_musician/<int:musician_id>/', views.unassoc_musician, name='unassoc_musician'),
  path('musicians/', views.MusicianList.as_view(), name='musicians_index'),
  path('musicians/<int:pk>/', views.MusicianDetail.as_view(), name='musicians_detail'),
  path('musicians/create/', views.MusicianCreate.as_view(), name='musicians_create'),
  path('musicians/<int:pk>/update/', views.MusicianUpdate.as_view(), name='musicians_update'),
  path('musicians/<int:pk>/delete/', views.MusicianDelete.as_view(), name='musicians_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]