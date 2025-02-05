from django.db.models import *

class Test(Model):
    num_of_questions_max = IntegerField(default=None)
    done = BooleanField(default=False)
    wrong_answers = IntegerField(default=0)


class Question(Model):
    test = ForeignKey(Test, on_delete=CASCADE)
    question_no = IntegerField()
    question_text = CharField(max_length=255)
    answer_a = CharField(max_length=255)
    answer_b = CharField(max_length=255)
    answer_c = CharField(max_length=255)
    correct_answer = CharField(max_length=255)
    picked_answer = CharField(max_length=255, default=None, null=True)

    def __str__(self):
        return f"{self.question_no})"