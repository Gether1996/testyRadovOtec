import json
from django.conf import settings
from django.http import JsonResponse
from viewer.models import Test, Question, FontSize
import random
import os

def check_answer(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            test_obj = Test.objects.first()
            try:
                question = Question.objects.get(id=json_data['question_id'])
                if str(getattr(question, str(json_data.get('picked_answer')))) == question.correct_answer:
                    question.delete()
                    test_obj.correct_answers += 1
                    test_obj.save()
                    return JsonResponse({'status': 'success'})
                else:
                    correct_field = next(
                        (field for field in ['answer_a', 'answer_b', 'answer_c']
                         if getattr(question, field, None) == question.correct_answer),
                        None
                    )
                    test_obj.wrong_answers += 1
                    test_obj.save()
                    return JsonResponse({'status': 'success', 'correct_answer': correct_field})

            except Question.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Otázka sa nenašla'})
        except Test.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Test sa nenašiel'})
    return JsonResponse({'status': 'error'})

def create_test(request):
    if request.method == 'POST':
        already_made_test = Test.objects.first()
        if already_made_test:
            already_made_test.delete()

        json_file_path = os.path.join(settings.BASE_DIR, 'Data', 'sbs_questions_p.json')

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            questions_to_create = []
            new_test = Test.objects.create(
                done=False,
                num_of_questions_max=len(data),
            )

            questions_counter = 1
            for question in data:
                answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                random.shuffle(answer_options)
                questions_to_create.append(Question(
                    test=new_test,
                    question_no=questions_counter,
                    question_text=question['question_text'],
                    answer_a=answer_options[0],
                    answer_b=answer_options[1],
                    answer_c=answer_options[2],
                    correct_answer=question['answer_a']
                ))
                questions_counter += 1

            Question.objects.bulk_create(questions_to_create)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def continue_test(request):
    if request.method == 'POST':
        existing_test = Test.objects.first()
        if existing_test:
            return JsonResponse({'status': 'success', 'max': existing_test.num_of_questions_max, 'progress': existing_test.correct_answers})
        else:
            return JsonResponse({'status': 'error', 'message': 'Test sa nenašiel, prosím vytvorte nový.'})
    return JsonResponse({'status': 'error'})

def save_font_size(request, chosen_size):
    if request.method == 'GET':
        current_size = FontSize.objects.first()
        current_size.size = int(chosen_size)
        current_size.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})