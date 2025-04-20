from django.db import models

class WorkoutVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text="Paste a YouTube embed link or watch link")

    def __str__(self):
        return self.title

    def get_video_id(self):
        """
        Extracts video ID from common YouTube URL formats.
        """
        if "embed/" in self.video_url:
            return self.video_url.split("embed/")[1].split("?")[0]
        elif "watch?v=" in self.video_url:
            return self.video_url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in self.video_url:
            return self.video_url.split("youtu.be/")[1].split("?")[0]
        return ""

