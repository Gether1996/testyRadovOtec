import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from viewer.models import Test, Question, PinCode, EmailInPV31, LectorPin, Course
import random
import hashlib
import string
import os
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


##############################################             RIP                   ####################################


# def find_question_by_question_no(questions_list, target_question_no):
#     for question in questions_list:
#         if question[0] == target_question_no:
#             return question
#     return None
#
#
# def correct_or_incorrect(request):
#     if request.method == 'POST':
#         user_progress_numbers = request.session.get('answered_questions', [])
#         wrong_answers_count = request.session.get('wrong_answers', 0)
#         post_data = json.loads(request.body.decode('utf-8'))
#         print(post_data["testName"])
#
#         questions_list = read_json_file_create_lists(f'Data/{str(post_data["testName"])}.json')
#         question_list = find_question_by_question_no(questions_list, int(post_data['questionNumber']))
#
#         if question_list[5] in post_data['answer']:
#             user_progress_numbers.append(int(post_data['questionNumber']))
#             print('correct_or_incorrect called -> correct answer!')
#             request.session['answered_questions'] = user_progress_numbers
#             request.session.save()
#             return JsonResponse({'status': 'correct'})
#         else:
#             wrong_answers_count += 1
#             print('correct_or_incorrect called -> wrong answer!')
#             request.session['wrong_answers'] = wrong_answers_count
#             request.session.save()
#             return JsonResponse({'status': 'incorrect', 'correct_answer': question_list[5]})
#
#
#
#
# def get_saved_questions(request):
#     questions = request.session.get('questions', None)
#     test_name = request.session.get('test_name', None)
#     print(f'get_saved_questions called -> saved questions in session: {questions}')
#     return JsonResponse({'questions': questions, 'test_name': test_name})
#
#
# def read_json_file_create_lists(json_file):
#     with open(json_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     questions_list = []
#
#     for question_data in data:
#         question_no = question_data['question_no']
#         question_text = question_data['question_text']
#         answer_a = question_data['answer_a']
#         answer_b = question_data['answer_b']
#         answer_c = question_data['answer_c']
#         correct_answer = question_data['answer_a']
#
#         question_list = [question_no, question_text, answer_a, answer_b, answer_c, correct_answer]
#
#         questions_list.append(question_list)
#     return questions_list
