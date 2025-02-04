import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from viewer.models import Test, Question, PinCode, EmailInPV31, LectorPin, Course
import random
import os
from .general import generate_random_8_pin, generate_hash_code


new_tests_count = getattr(settings, 'NUMBER_OF_NEW_TESTS_PER_PIN')
questions_count = getattr(settings, 'QUESTION_COUNT_PER_TEST')


def create_tests(request):
    if request.method == 'POST':

        pin_obj = PinCode.objects.create(
            pin=generate_random_8_pin(),
            hash=generate_hash_code(),
        )

        json_file_path = os.path.join(settings.BASE_DIR, 'Data', 'sbs_questions_s.json')

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            questions_1_to_100 = data[0:100]
            questions_101_to_200 = data[100:200]
            questions_201_to_250 = data[200:250]

            questions_to_create = []

            for new_test_number in range(1, new_tests_count + 1):
                questions_counter = 1

                new_test = Test.objects.create(
                    order=new_test_number,
                    pin=pin_obj,
                )

                random_10_questions_1_100 = random.sample(questions_1_to_100, 10)
                random_20_questions_101_200 = random.sample(questions_101_to_200, 20)
                random_10_questions_201_250 = random.sample(questions_201_to_250, 10)

                for question in random_10_questions_1_100:
                    answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                    random.shuffle(answer_options)
                    questions_to_create.append(Question(
                        test=new_test,
                        question_no=questions_counter,
                        question_text=question['question_text'],
                        point_value=1,
                        answer_a=answer_options[0],
                        answer_b=answer_options[1],
                        answer_c=answer_options[2],
                        correct_answer=question['answer_a']
                    ))
                    questions_counter += 1

                for question in random_20_questions_101_200:
                    answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                    random.shuffle(answer_options)
                    questions_to_create.append(Question(
                        test=new_test,
                        question_no=questions_counter,
                        question_text=question['question_text'],
                        point_value=2,
                        answer_a=answer_options[0],
                        answer_b=answer_options[1],
                        answer_c=answer_options[2],
                        correct_answer=question['answer_a']
                    ))
                    questions_counter += 1

                for question in random_10_questions_201_250:
                    answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                    random.shuffle(answer_options)
                    questions_to_create.append(Question(
                        test=new_test,
                        question_no=questions_counter,
                        question_text=question['question_text'],
                        point_value=3,
                        answer_a=answer_options[0],
                        answer_b=answer_options[1],
                        answer_c=answer_options[2],
                        correct_answer=question['answer_a']
                    ))
                    questions_counter += 1

            Question.objects.bulk_create(questions_to_create)

        return JsonResponse({'status': 'success', 'pin': pin_obj.pin, 'pin_hash': pin_obj.hash})
    return JsonResponse({'status': 'error'})


def create_students(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        course_obj = Course.objects.get(pin=json_data['course_pin'])

        number_of_students = json_data['number_of_students']
        json_file_path = os.path.join(settings.BASE_DIR, 'Data', 'sbs_questions_s.json')

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            questions_1_to_100 = data[0:100]
            questions_101_to_200 = data[100:200]
            questions_201_to_250 = data[200:250]

        for num in range(1, int(number_of_students) + 1):
            existing_pin_obj_order = PinCode.objects.filter(course_pin=course_obj).last().order
            pin_obj = PinCode.objects.create(
                pin=generate_random_8_pin(),
                hash=generate_hash_code(),
                course_pin=course_obj,
                order=(existing_pin_obj_order + 1) if existing_pin_obj_order else 1
            )

            questions_to_create = []

            for new_test_number in range(1, new_tests_count + 1):
                questions_counter = 1

                new_test = Test.objects.create(
                    order=new_test_number,
                    pin=pin_obj,
                )

                random_10_questions_1_100 = random.sample(questions_1_to_100, 10)
                random_20_questions_101_200 = random.sample(questions_101_to_200, 20)
                random_10_questions_201_250 = random.sample(questions_201_to_250, 10)

                for question in random_10_questions_1_100:
                    answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                    random.shuffle(answer_options)
                    questions_to_create.append(Question(
                        test=new_test,
                        question_no=questions_counter,
                        question_text=question['question_text'],
                        point_value=1,
                        answer_a=answer_options[0],
                        answer_b=answer_options[1],
                        answer_c=answer_options[2],
                        correct_answer=question['answer_a']
                    ))
                    questions_counter += 1

                for question in random_20_questions_101_200:
                    answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                    random.shuffle(answer_options)
                    questions_to_create.append(Question(
                        test=new_test,
                        question_no=questions_counter,
                        question_text=question['question_text'],
                        point_value=2,
                        answer_a=answer_options[0],
                        answer_b=answer_options[1],
                        answer_c=answer_options[2],
                        correct_answer=question['answer_a']
                    ))
                    questions_counter += 1

                for question in random_10_questions_201_250:
                    answer_options = [question['answer_a'], question['answer_b'], question['answer_c']]
                    random.shuffle(answer_options)
                    questions_to_create.append(Question(
                        test=new_test,
                        question_no=questions_counter,
                        question_text=question['question_text'],
                        point_value=3,
                        answer_a=answer_options[0],
                        answer_b=answer_options[1],
                        answer_c=answer_options[2],
                        correct_answer=question['answer_a']
                    ))
                    questions_counter += 1

            Question.objects.bulk_create(questions_to_create)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def change_name_surname_pin(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        new_name_surname = json_data['new_name']
        pin_code = get_object_or_404(PinCode, pk=json_data['pin_id'])
        pin_code.name_surname = new_name_surname
        pin_code.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def delete_pin(request):
    if request.method == 'DELETE':
        json_data = json.loads(request.body.decode('utf-8'))
        pin_to_delete = PinCode.objects.get(id=json_data['pin_id'])
        pin_to_delete.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def create_course(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        new_course = Course.objects.create(
            name=json_data['course_name'],
            pin=generate_random_8_pin(),
            start=json_data['starting_date'],
            hash=generate_hash_code()
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def change_name_start_course(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        try:
            course = Course.objects.get(id=json_data['course_id'])
            course.name = json_data['new_name']
            course.start = json_data['new_start']
            course.save()
            return JsonResponse({'status': 'success'})
        except Course.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Kurz sa nenašiel'})
    return JsonResponse({'status': 'error'})


def delete_course(request):
    if request.method == 'DELETE':
        json_data = json.loads(request.body.decode('utf-8'))
        course_to_delete = Course.objects.get(id=json_data['course_id'])
        course_to_delete.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})