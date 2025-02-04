import json
from django.http import JsonResponse
from viewer.models import Test, Question

# def login_with_pin(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#         try:
#             pin_obj = PinCode.objects.get(pin=json_data['pin'])
#
#             return JsonResponse({'status': 'success', 'hash': pin_obj.hash})
#
#         except PinCode.DoesNotExist:
#             return JsonResponse({'status': 'error'})
#     return JsonResponse({'status': 'error'})
#
#
# def login_lector(request):
#     if request.method == 'POST':
#         json_data = json.loads(request.body.decode('utf-8'))
#
#         try:
#             lector = LectorPin.objects.get(pin=json_data['pin'])
#             return JsonResponse(
#                 {'status': 'success', 'message': 'Prihlásenie úspešné.', 'user': 'lector', 'hash': lector.hash})
#
#         except LectorPin.DoesNotExist:
#             try:
#                 course = Course.objects.get(pin=json_data['pin'])
#                 return JsonResponse(
#                     {'status': 'success', 'message': 'Prihlásenie úspešné.', 'user': 'course', 'hash': course.hash})
#
#             except Course.DoesNotExist:
#                 return JsonResponse({'status': 'error', 'message': 'Nesprávny PIN.'})

def check_correct(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        try:
            question = Question.objects.get(id=json_data['question_id'])
            if str(json_data['picked_answer']) == question.correct_answer:
                question.delete()
                return JsonResponse({'status': 'success'})

            else:
                return JsonResponse({'status': 'success', 'correct_answer': question.correct_answer})

        except Question.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Otázka sa nenašla'})
    return JsonResponse({'status': 'error'})