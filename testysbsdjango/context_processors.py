from viewer.models import FontSize, Test

def get_font_size(request):
    current_font_size = FontSize.objects.first()
    return {'current_font_size': current_font_size.size}

def get_test_with_progress(request):
    existing_test = Test.objects.first()
    returning_text = ""
    if existing_test and existing_test.correct_answers > 0:
        returning_text = f"Zodpovedaných {existing_test.correct_answers} z {existing_test.num_of_questions_max} otázok"
    return {'progress_text': returning_text}