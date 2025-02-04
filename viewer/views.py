from django.shortcuts import render
from viewer.models import Test, Question
import random

def homepage(request):
    return render(request, 'homepage.html')

def test(request):
    test_obj = Test.objects.first()
    if not test_obj:
        return render(request, 'error.html', {'error': 'Test sa nenašiel.'})
    test_name = 'Preukaz SBS - P'

    remaining_questions = list(Question.objects.filter(test=test_obj))
    current_question = random.choice(remaining_questions) if remaining_questions else None

    all_questions = test_obj.num_of_questions_max
    filled_questions = all_questions - len(remaining_questions)

    context = {
        'test_obj': test_obj,
        'all_questions': all_questions,
        'current_question': current_question,
        'filled_questions': filled_questions,
        'test_name': test_name,
        'user_progress': filled_questions,
        'remaining_questions': len(remaining_questions),
        'done_questions_percent': round((filled_questions / all_questions * 100), 2),
    }

    return render(request, 'test.html', context)