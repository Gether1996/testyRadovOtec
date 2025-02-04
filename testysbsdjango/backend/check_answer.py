import json
from django.http import JsonResponse
from viewer.models import Question

def check_correct(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        try:
            question = Question.objects.get(id=json_data['question_id'])
            if str(getattr(question, str(json_data.get('picked_answer')))) == question.correct_answer:
                question.delete()
                return JsonResponse({'status': 'success'})

            else:
                correct_field = next(
                    (field for field in ['answer_a', 'answer_b', 'answer_c']
                     if getattr(question, field, None) == question.correct_answer),
                    None
                )

                return JsonResponse({'status': 'success', 'correct_answer': correct_field})

        except Question.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Otázka sa nenašla'})
    return JsonResponse({'status': 'error'})