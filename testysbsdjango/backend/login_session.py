import json
from django.http import JsonResponse
from viewer.models import Test, Question, PinCode, EmailInPV31, LectorPin, Course
from .general import initialize_timer


def login_with_pin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            pin_obj = PinCode.objects.get(pin=json_data['pin'])

            return JsonResponse({'status': 'success', 'hash': pin_obj.hash})

        except PinCode.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


def login_lector(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        try:
            lector = LectorPin.objects.get(pin=json_data['pin'])
            return JsonResponse(
                {'status': 'success', 'message': 'Prihlásenie úspešné.', 'user': 'lector', 'hash': lector.hash})

        except LectorPin.DoesNotExist:
            try:
                course = Course.objects.get(pin=json_data['pin'])
                return JsonResponse(
                    {'status': 'success', 'message': 'Prihlásenie úspešné.', 'user': 'course', 'hash': course.hash})

            except Course.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Nesprávny PIN.'})


def delete_session(request):
    if request.method == 'POST':
        request.session.flush()
        initialize_timer(request)
        print('delete_session called -> Session deleted and timer reseted')
        return JsonResponse({'status': 'success'})


def save_progress_into_session(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        filled_questions = request.session.get('filled_questions', [])
        new_input_pair = [int(json_data['question_id']), str(json_data['picked_answer'])]
        changed_already_in_session = False
        new_questions = []

        if filled_questions:
            for pair in filled_questions:
                if pair[0] == new_input_pair[0]:
                    pair[1] = new_input_pair[1]
                    new_questions.append(pair)
                    changed_already_in_session = True
                else:
                    new_questions.append(pair)

        if not changed_already_in_session:
            new_questions.append(new_input_pair)

        request.session['filled_questions'] = new_questions
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})