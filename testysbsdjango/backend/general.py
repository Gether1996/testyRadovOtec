import json
from django.conf import settings
from django.http import JsonResponse
from viewer.models import Test, Question
import random
import hashlib
import string
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string


# def generate_random_8_pin():
#     return random.randint(10000000, 99999999)
#
#
# def generate_hash_code():
#     random_string = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12))
#     random_hash = hashlib.sha256(random_string.encode('utf-8')).hexdigest()
#     truncated_hash = random_hash[:12]
#     hash_with_hyphens = '-'.join([truncated_hash[i:i + 4] for i in range(0, len(truncated_hash), 4)])
#
#     return hash_with_hyphens
#
#
# def initialize_timer(request):
#     current_time = timezone.now()
#     end_time = current_time + timedelta(minutes=getattr(settings, 'TEST_DURATION_IN_MINUTES'))
#
#     request.session['timer_end'] = end_time.isoformat()
#     request.session.save()
#     print(f'Nový timer {end_time.isoformat()}')


# def send_email(request):
#     if request.method == 'POST':
#         from_email = str(getattr(settings, 'EMAIL_HOST'))
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#
#         pin_obj = PinCode.objects.get(hash=json_data['pin_hash'])
#
#         html_message = render_to_string('send_email.html', {'pin_obj': pin_obj})
#
#         email_to_pv31 = EmailInPV31.objects.using('ccsi_db').create(
#             subject='Testy SBS - pin kód',
#             from_email=from_email,
#             to_email=json_data['email'],
#             message=html_message
#         )
#
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def finish_test(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))

            test_obj = Test.objects.first()
            questions = Question.objects.filter(test=test_obj)
            user_filled_questions = request.session.get('filled_questions', [])

            points_obtained = 0
            for filled_pair in user_filled_questions:
                question_id, user_answer = filled_pair
                try:
                    question = questions.get(id=question_id)
                    picked_answer_text = getattr(question, user_answer)
                    question.picked_answer = picked_answer_text
                    question.save()
                    if picked_answer_text == question.correct_answer:
                        points_obtained += question.point_value
                except Question.DoesNotExist:
                    print(f'Question with id {question_id} does not exist in this test.')

            test_obj.points = points_obtained
            test_obj.done = True
            test_obj.save()
            request.session.flush()

            return JsonResponse({'status': 'success', 'points': points_obtained})
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})