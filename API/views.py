from django.http import JsonResponse
from django.views import View
import os
import json
import datetime

QUESTIONS_S_FILE = "Data/sbs_questions_s.json"
QUESTIONS_P_FILE = "Data/sbs_questions_p.json"


class GetLastChangeView(View):
    def get(self, request, *args, **kwargs):
        last_change_s = self.get_last_modified_time(QUESTIONS_S_FILE)
        last_change_p = self.get_last_modified_time(QUESTIONS_P_FILE)

        data = {
            "last_change_s": last_change_s,
            "last_change_p": last_change_p
        }

        return JsonResponse(data)

    def get_last_modified_time(self, file_path):
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            last_modified_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return last_modified_time
        else:
            return None


class GetQuestionsSView(View):
    def get(self, request, *args, **kwargs):
        questions_s = self.read_json_file(QUESTIONS_S_FILE)
        if questions_s is not None:
            return JsonResponse({"questions_s": questions_s}, safe=False)
        else:
            return JsonResponse({"error": "File not found or invalid format"}, status=500)

    def read_json_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    return data
                except json.JSONDecodeError:
                    return None
        else:
            return None


class GetQuestionsPView(View):
    def get(self, request, *args, **kwargs):
        questions_p = self.read_json_file(QUESTIONS_P_FILE)
        if questions_p is not None:
            return JsonResponse({"questions_p": questions_p}, safe=False)
        else:
            return JsonResponse({"error": "File not found or invalid format"}, status=500)

    def read_json_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    return data
                except json.JSONDecodeError:
                    return None
        else:
            return None
