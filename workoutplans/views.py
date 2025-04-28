from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import WorkoutPlanForm
from .models import WorkoutPlan
from .utils import generate_workout_plan


@login_required
def workout_plan_request(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            user_input = f"""
            Fitness Level: {form.cleaned_data['fitness_level']}
            Goal: {form.cleaned_data['goal']}
            Session Duration: {form.cleaned_data['session_duration']} minutes
            Days per Week: {form.cleaned_data['days_per_week']}
            Equipment Available: {', '.join(form.cleaned_data['equipment'])}
            Injuries: {form.cleaned_data['injuries']}
            Preferences: {form.cleaned_data['preferences']}
            Additional Notes: {form.cleaned_data['additional_notes']}
            """

            generated_plan = generate_workout_plan(user_input)

            if generated_plan:
                request.session['generated_plan'] = generated_plan
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('workoutplans:results')
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False})
                messages.error(request, "Failed to generate plan. Please try again.")
                return redirect('workoutplans:request')
    else:
        form = WorkoutPlanForm()

    return render(request, 'workoutplans/request.html', {'form': form})


@login_required
def workout_plan_results(request):
    generated_plan = request.session.get('generated_plan', None)

    if not generated_plan:
        messages.warning(request, "No workout plan generated yet.")
        return redirect('workoutplans:request')

    return render(request, 'workoutplans/results.html', {'plan': generated_plan})


@login_required
@require_POST
def save_plan(request):
    plan_text = request.session.get('generated_plan')
    title = request.POST.get('title', 'My Custom Workout Plan')  # fallback

    if plan_text:
        WorkoutPlan.objects.create(
            user=request.user,
            title=title,
            content=plan_text
        )
        messages.success(request, "Workout plan saved successfully!")
    else:
        messages.error(request, "No workout plan to save.")

    return redirect('workoutlog:user_dashboard')


@login_required
def saved_plans(request):
    plans = WorkoutPlan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'workoutplans/saved_list.html', {'plans': plans})


@login_required
def delete_plan(request, plan_id):
    plan = get_object_or_404(WorkoutPlan, id=plan_id, user=request.user)
    plan.delete()
    messages.success(request, "Workout plan deleted successfully.")
    return redirect('workoutplans:saved_list')


@login_required
def view_plan(request, plan_id):
    plan = get_object_or_404(WorkoutPlan, id=plan_id, user=request.user)
    return render(request, 'workoutplans/view_plan.html', {'plan': plan})
