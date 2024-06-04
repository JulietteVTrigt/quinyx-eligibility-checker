from django.db import models

# Create your models here.


class AutoAssignProblem(models.Model):
    shift_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    client_secret = models.CharField(max_length=50)
    payload = models.TextField()

    def __str(self):
        return self.shift_id


class EligibilityCheck(models.Model):
    eligible_by_agreement = models.BooleanField(default=False)
    employee_has_required_active_departments = models.BooleanField(default=False)
    shift_within_availabilities = models.BooleanField(default=False)
    shift_outside_unavailabilities = models.BooleanField(default=False)
    eligible_by_contract_coverage = models.BooleanField(default=False)
    eligible_by_shift_departments = models.BooleanField(default=False)
    eligible_by_shift_skills = models.BooleanField(default=False)
    eligible_by_shift_licences = models.BooleanField(default=False)

    def __str(self):
        return self.user_id
