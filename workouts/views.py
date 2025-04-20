from django.shortcuts import render, get_object_or_404
from .models import WorkoutVideo

def video_list(request):
    videos = WorkoutVideo.objects.all()
    return render(request, 'workouts/video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(WorkoutVideo, pk=pk)
    return render(request, 'workouts/video_detail.html', {'video': video})
