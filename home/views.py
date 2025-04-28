from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from profiles.models import Profile  # 🛠 import Profile instead!
from messaging.models import Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random


def index(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    return render(request, 'home/index.html', {
        'template_data': {
            'title': 'FitJacket',
        },
        'unread_count': unread_count
    })


def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def feed(request):
    # 🛠 Get all profiles where role = 'trainer'
    trainers = Profile.objects.filter(role='trainer').select_related('user')
    return render(request, 'home/feed.html', {'trainers': trainers})

MESSAGES = [
    "Keep going, you're unstoppable! 🚀",
    "Your hard work will pay off! 💥",
    "Never give up, you're almost there! 🛤️",
    "Small steps every day lead to big changes! 🏋️",
    "You don’t have to be great to start, but you have to start to be great. 💪",
    "Every rep, every set, every workout gets you closer to your goal. 🏋️‍♀️",
    "Progress is progress, no matter how small. 🌱",
    "Feel the burn; that’s your body getting stronger. 🔥",
    "If you’re tired of starting over, stop giving up. 💥",
    "Discipline is the bridge between goals and accomplishment. 🏆",
    "Success starts with self-discipline. 💯",
    "Don’t limit your challenges. Challenge your limits. 🚀",
    "Excuses don’t burn calories. ❌🔥",
    "Train insane or remain the same. 😤",
    "A year from now, you’ll wish you had started today. ⏳",
    "The pain you feel today will be the strength you feel tomorrow. 💪🔥",
    "The hardest lift of all is lifting your butt off the couch. 😅",
    "The difference between try and triumph is just a little umph! 💥",
    "You are stronger than you think. 💪",
    "Focus on progress, not perfection. 🎯",
    "You don’t have to go fast, you just have to go. 🚶‍♂️",
    "Your body can stand almost anything. It’s your mind that you have to convince. 🧠💪",
    "Do something today that your future self will thank you for. 🙌",
    "The only bad workout is the one you didn’t do. ❌🏋️‍♀️",
    "Consistency is key—don’t aim for perfection, just show up every day. 🔑",
    "You are capable of more than you think. 🌟",
    "Set goals, crush them, then set bigger ones. 🎯",
    "One workout at a time, one day at a time. 🗓️",
    "Train hard, stay focused, and the results will follow. 🏅",
    "Your fitness journey isn’t about being better than someone else, it’s about being better than you were yesterday. 🚶‍♀️📈",
    "The only way to finish is to start. ✅",
    "It’s not about being the best, it’s about being better than you were yesterday. 🔝",
    "Success starts with taking the first step. 👣",
    "Fitness is not about being better than someone else; it’s about being better than you used to be. 🔥",
    "Remember to hydrate! Water is essential for peak performance. 💧",
    "Warm up properly—prevent injuries and boost your performance. 🏃‍♂️",
    "Don’t skip your cool-down—stretching is just as important as the workout itself. 🤸‍♀️",
    "Set realistic goals and celebrate each milestone, no matter how small. 🎉",
    "Rest is just as important as the workout. Your muscles grow during recovery. 🛌"

]

@api_view(['GET'])
def motivational_message(request):
    message = random.choice(MESSAGES)
    return Response({'message': message})
