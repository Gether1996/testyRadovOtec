from django.db.models import *


# class LectorPin(Model):
#     pin = IntegerField(unique=True)
#     hash = CharField(max_length=150, unique=True, default=None, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.pin)
#
#
# class Course(Model):
#     pin = IntegerField(unique=True)
#     name = CharField(max_length=100)
#     start = DateField()
#     hash = CharField(max_length=150, unique=True)
#
#
# class PinCode(Model):
#     pin = IntegerField(unique=True)
#     hash = CharField(max_length=150, unique=True)
#     active = BooleanField(default=True)
#     course_pin = ForeignKey(Course, null=True, blank=True, on_delete=CASCADE, default=None)
#     name_surname = CharField(max_length=100, default=None, null=True, blank=True)
#     order = IntegerField(default=None, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.pin)


class Test(Model):
    # order = IntegerField()
    # pin = ForeignKey(PinCode, on_delete=CASCADE)
    # active = BooleanField(default=True)
    done = BooleanField(default=False)

    def __str__(self):
        return f'({self.pin.pin}) - test n. {self.order}'

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

    def correctly_answered(self):
        if self.picked_answer:
            if self.picked_answer == self.correct_answer:
                return True
        return False


# class EmailInPV31(Model):
#     from_email = CharField(max_length=200, db_column='from_mail')
#     to_email = CharField(max_length=1000, db_column='to_mail')
#     subject = CharField(max_length=200, db_column='subject')
#     message = CharField(max_length=1000, db_column='message')
#
#     class Meta:
#         db_table = 'srv_sendmails_multiple'
#         app_label = 'viewer'
#         managed = False