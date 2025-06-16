from django.db import models


# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/')
    audio_file = models.FileField(upload_to='audio_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    video_file = models.FileField(upload_to='video/', blank=True, null=True)
    lyrics_file = models.FileField(upload_to='lyrics/', blank=True, null=True)


    def __str__(self):
        return f"{self.title} by {self.artist}"

    def audio_file_size_mb(self):
        if self.audio_file:
            return round(self.audio_file.size / (1024 * 1024), 2)
        return 0

    def video_file_size_mb(self):
        if self.video_file:
            return round(self.video_file.size / (1024 * 1024), 2)
        return 0

    def lyrics_file_size_kb(self):
        if self.lyrics_file:
            return round(self.lyrics_file.size / 1024, 2)
        return 0

