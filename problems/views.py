from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem
from django.template import loader
from django.http import HttpResponse

# Create your views here.


@login_required
def problem_list(request):
    topics = Problem.objects.values_list('topic', flat=True).distinct()
    levels = ['Easy', 'Medium', 'Hard']  # List of available levels

    problems = Problem.objects.all()

    # Filter by topic
    topic_filter = request.GET.get('topic')
    if topic_filter:
        problems = problems.filter(topic=topic_filter)

    # Filter by level
    level_filter = request.GET.get('level')
    if level_filter in ['Easy', 'Medium', 'Hard']:
        problems = problems.filter(level=level_filter)

    # Default values for topic and level dropdowns
    selected_topic = topic_filter if topic_filter else ""
    selected_level = level_filter if level_filter in ['Easy', 'Medium', 'Hard'] else ""

    context = {
        'problems': problems,
        'topics': topics,
        'levels': levels,
        'selected_topic': selected_topic,
        'selected_level': selected_level,
    }
    return render(request, 'problem_list.html', context)
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, unique_id=pk)
    context = {
        'problem': problem,
    }
    return render(request, 'problem_detail.html', context)



