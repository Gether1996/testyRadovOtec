import json
from django.conf import settings
from django.http import JsonResponse
from viewer.models import Test, Question
import random
import os

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
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Test sa nenašiel, prosím vytvorte nový.'})
    return JsonResponse({'status': 'error'})