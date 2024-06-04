from django.shortcuts import render
from django.http import HttpResponse
from .eligibility_checker.check_eligibility import EligibilityChecker
import json


def home(response):
    return render(response, "main/home.html", {"name": "Home"})


def eligibility_check_page(response):
    return render(response, "main/eligibility_checker.html", {"name": "Eligibility Check"})


def violation_comparator_page(response):
    return render(response, "main/violation_comparator.html", {"name": "Violation Comparator"})


def eligibility_check(request):
    if request.method == 'POST':
        shift_id = request.POST.get('shift_id')
        user_id = request.POST.get('user_id')
        run_id = request.POST.get('run_id')

        if not shift_id or not user_id or not run_id:
            missing_fields = [
                field for field in ['shift_id', 'user_id', 'run_id'] if not request.POST.get(field)
            ]

            return render(request, "main/view_result.html", {"reasons": missing_fields})
            # Probably should have different response for missing fields!

        eligibility_checker = EligibilityChecker(run_id, shift_id, user_id)
        reasons = eligibility_checker.check_eligibility()
        return render(request, "main/view_result.html", {"reasons": reasons})
    else:
        return HttpResponse("Invalid request method")


def violation_comparator(request):
    # TODO: implement this logic
    if request.method == 'POST':
        file = request.FILES['file']
        file_content = file.read().decode('utf-8')
        payload = json.loads(file_content)
        eligibility_checker = EligibilityChecker(payload, 8563973, 81347)
        reasons = eligibility_checker.check_eligibility()
        return render(request, "main/view_result.html", {"reasons": reasons})
    else:
        return HttpResponse("Invalid request method")