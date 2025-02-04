from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from viewer.models import Test, Question, PinCode, LectorPin, Course
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from unidecode import unidecode

lector_pin = getattr(settings, 'LECTOR_PIN')

def homepage(request):
    return render(request, 'homepage.html')


def my_tests(request, hash):
    try:
        pin_obj = PinCode.objects.get(hash=hash)
        tests = Test.objects.filter(pin=pin_obj, active=True)
        done_tests = tests.filter(done=True, points__gte=64).count()

        context = {
            'pin_obj': pin_obj,
            'lector_logged': False,
            'tests': tests,
            'hash': hash,
            'user_progress': done_tests,
            'remaining_tests': len(tests) - done_tests,
            'done_tests_percent': int((done_tests / len(tests)) * 100),
        }

        return render(request, 'my_tests.html', context)
    except PinCode.DoesNotExist:
        return render(request, 'error.html', {'error': 'Pin sa nenašiel.'})


def test(request, hash, test_number, question_number):
    timer = request.session.get('timer_end', None)

    try:
        pin_obj = PinCode.objects.get(hash=hash)
    except PinCode.DoesNotExist:
        return render(request, 'error.html', {'error': 'Pin sa nenašiel.'})

    test_obj = Test.objects.get(order=test_number, pin=pin_obj)
    test_name = 'Preukaz SBS - S'

    all_questions = Question.objects.filter(test=test_obj)
    filled_questions = request.session.get('filled_questions', [])

    try:
        current_question = all_questions.get(question_no=question_number)
    except Question.DoesNotExist:
        return render(request, 'error.html', {'error': 'Test sa nenašiel.'})

    context = {
        'pin_obj': pin_obj,
        'test_obj': test_obj,
        'all_questions': all_questions,
        'current_question': current_question,
        'filled_questions': filled_questions,
        'test_name': test_name,
        'user_progress': len(filled_questions),
        'remaining_questions': len(all_questions) - len(filled_questions),
        'done_questions_percent': int((len(filled_questions) / len(all_questions)) * 100),
        'hash': hash,
        'timer': timer,
    }

    return render(request, 'test.html', context)


def test_history(request, hash, test_number):
    try:
        pin_obj = PinCode.objects.get(hash=hash)
    except PinCode.DoesNotExist:
        return render(request, 'error.html', {'error': 'Pin sa nenašiel.'})

    test_obj = Test.objects.get(order=test_number, pin=pin_obj)
    all_questions = Question.objects.filter(test=test_obj)

    context = {
        'pin_obj': pin_obj,
        'lector_logged': False,
        'test_obj': test_obj,
        'all_questions': all_questions,
        'hash': hash,
    }

    return render(request, 'test_history.html', context)


def lector_view(request, lector_hash):
    try:
        lector = LectorPin.objects.get(hash=lector_hash)
        all_course_objects = Course.objects.annotate(pin_count=Count('pincode'))
        input_from_search = request.GET.get('input_from_search', None)
        sort_by = request.GET.get('sort_by', 'pin')
        order = request.GET.get('order', 'asc')

        if order == 'asc' and sort_by:
            all_course_objects = all_course_objects.order_by(str(sort_by))
        elif order == 'desc' and sort_by:
            all_course_objects = all_course_objects.order_by(f'-{sort_by}')

        if input_from_search:
            filtered_course_objects = []
            for course_obj in all_course_objects:
                formatted_start_date = course_obj.start.strftime('%d.%m.%Y')
                if (
                    input_from_search in str(course_obj.pin) or
                    unidecode(input_from_search.lower()) in unidecode(course_obj.name.lower()) or
                    input_from_search in formatted_start_date or
                    input_from_search in str(course_obj.pin_count)
                ):
                    filtered_course_objects.append(course_obj)

            all_course_objects = filtered_course_objects
        filter_parameters = {'input_from_search': input_from_search}

        paginator = Paginator(all_course_objects, getattr(settings, 'COURSES_PER_PAGE'))
        page = request.GET.get('page')
        try:
            loaded_courses = paginator.page(page)
        except PageNotAnInteger:
            loaded_courses = paginator.page(1)
        except EmptyPage:
            loaded_courses = paginator.page(paginator.num_pages)

        courses_data = [
            {
                'id': course.id,
                'name': course.name,
                'start': course.start,
                'pin': course.pin,
                'hash': course.hash,
                'pin_count': course.pin_count,
            }
            for course in loaded_courses
        ]

        context = {
            'lector': lector,
            'lector_logged': True,
            'all_courses': courses_data,
            'filter_on': input_from_search,
            'current_sort_by': sort_by,
            'current_order': order,
            'filter_parameters': filter_parameters,
            'loaded_courses': loaded_courses,
        }

        url = reverse('lector_view', args=[lector_hash])
        url += '?sort_by=pin&order=asc'

        if 'sort_by' not in request.GET:
            return redirect(url)
        return render(request, 'lector_view.html', context)
    except LectorPin.DoesNotExist:
        return render(request, 'error.html', {'error': 'Lektor sa nenašiel.'})


def course_view(request, course_hash, lector_hash=None):
    lector = LectorPin.objects.get(hash=lector_hash) if lector_hash else None
    try:
        course = Course.objects.get(hash=course_hash)
        all_course_pins = PinCode.objects.filter(course_pin=course)
        input_from_search = request.GET.get('input_from_search', None)
        sort_by = request.GET.get('sort_by', 'order')
        order = request.GET.get('order', 'asc')

        if order == 'asc' and sort_by:
            all_course_pins = all_course_pins.order_by(str(sort_by))
        elif order == 'desc' and sort_by:
            all_course_pins = all_course_pins.order_by(f'-{sort_by}')

        if input_from_search:
            filtered_pin_objects = []
            for pin_obj in all_course_pins:

                if (
                    input_from_search in str(pin_obj.order) + '.' or
                    input_from_search.lower() in str(pin_obj.pin) or
                    input_from_search.lower() in str(pin_obj.name_surname).lower()
                ):
                    filtered_pin_objects.append(pin_obj)

            all_course_pins = filtered_pin_objects
        filter_parameters = {'input_from_search': input_from_search}

        paginator = Paginator(all_course_pins, getattr(settings, 'PINS_PER_PAGE'))
        page = request.GET.get('page')
        try:
            loaded_pins = paginator.page(page)
        except PageNotAnInteger:
            loaded_pins = paginator.page(1)
        except EmptyPage:
            loaded_pins = paginator.page(paginator.num_pages)

        course_pins_and_tests = []
        for pin in loaded_pins:
            tests = list(pin.test_set.all())
            specific_order_due_to_html = [tests[0], tests[5], tests[1], tests[6], tests[2], tests[7], tests[3], tests[8], tests[4], tests[9]]
            course_pins_and_tests.append({
                'pin': pin,
                'tests': specific_order_due_to_html
            })

        context = {
            'lector': lector,
            'course': course,
            'course_pins_and_tests': course_pins_and_tests,
            'lector_logged': True,
            'filter_parameters': filter_parameters,
            'loaded_pins': loaded_pins,
            'filter_on': input_from_search,
            'current_sort_by': sort_by,
            'current_order': order,
        }

        if lector_hash:
            url = reverse('course_view', args=[course_hash, lector_hash])
        else:
            url = reverse('course_view', args=[course_hash])
        url += '?sort_by=order&order=asc'

        if 'sort_by' not in request.GET:
            return redirect(url)
        return render(request, 'course_view.html', context)
    except LectorPin.DoesNotExist:
        return render(request, 'error.html', {'error': 'Kurz sa nenašiel.'})


def test_overview_course(request, course_hash, pin_hash, test_num):
    try:
        course_obj = Course.objects.get(hash=course_hash)
        pin_obj = PinCode.objects.get(hash=pin_hash, course_pin=course_obj)

    except LectorPin.DoesNotExist:
        return render(request, 'error.html', {'error': 'Kurz sa nenašiel.'})

    except PinCode.DoesNotExist:
        return render(request, 'error.html', {'error': 'Pin sa nenašiel.'})

    test_obj = Test.objects.get(order=test_num, pin=pin_obj)
    all_questions = Question.objects.filter(test=test_obj)

    context = {
        'course': course_obj,
        'lector_logged': True,
        'pin_obj': pin_obj,
        'test_obj': test_obj,
        'all_questions': all_questions,
    }

    return render(request, 'test_overview_course.html', context)