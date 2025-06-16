import os

from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.http import HttpResponse, Http404
import zipfile
import io
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import chain
from .models import Song
from django.shortcuts import render


def home(request):
    genre = request.GET.get('genre')
    query = request.GET.get('q')
    songs = Song.objects.all()

    if genre:
        songs = songs.filter(genre__iexact=genre)
    if query:
        songs = songs.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query)
        )

    latest_songs = Song.objects.all().order_by('-uploaded_at')[:6]
    trending_songs = Song.objects.all().order_by('-downloads')[:6]
    combined_songs = list(chain(latest_songs, trending_songs))

    if query or genre:
        paginator = Paginator(songs, 12)
    else:
        paginator = Paginator(combined_songs, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_downloads = Song.objects.order_by('-downloads')[:5]

    return render(request, 'home.html', {
        'songs': page_obj,
        'query': query,
        'genre': genre,
        'top_downloads': top_downloads,
        'latest_songs': latest_songs,
        'trending_songs': trending_songs,
    })


def is_uploader(user):
    return user.groups.filter(name='Uploaders').exists()



def download_song(request, song_id):
    song = Song.objects.get(pk=song_id)
    song.downloads += 1
    song.save()
    file_path = song.audio_file.path

    return FileResponse(open(file_path, 'rb'), as_attachment=True,filename=os.path.basename(file_path))

def download_options(request, music_id):
    music = get_object_or_404(Song, id=music_id)
    return render(request, 'music/download_options.html', {'music': music})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def FAQ(request):
    return render(request, 'FAQ.html')


def download_multiple(request):
    song_ids = request.GET.getlist('song_ids')
    if not song_ids:
        raise Http404("No songs selected")
    songs = Song.objects.filter(id__in=song_ids)
    if not songs:
        raise Http404("Songs not found")


    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for song in songs:
            song_file = song.audio_file.path
            zip_file.write(song_file, song.title + ".mp3")
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=songs.zip'
    return response

