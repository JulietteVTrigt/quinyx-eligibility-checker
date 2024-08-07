import json
from .external.alfa import AlfaClient


class EligibilityChecker:
    def __init__(self, run_id, shift_id, user_id, alfa_client_id=None, alfa_client_secret=None):
        self.alfa = AlfaClient(
            alfa_client_id,
            alfa_client_secret
        )

        payload = self._get_run_by_id(run_id)
        self.shifts = payload["shifts"]
        self.employees = payload["users"]
        self.rules = payload["rules"]
        self.settings = payload["settings"]
        self.shift_id = int(shift_id)
        self.user_id = int(user_id)

    def _get_run_by_id(self, run_id):
        output = self.alfa.poll_problem(run_id)
        return output

    def _get_shift_from_payload(self):
        for shift in self.shifts:
            if shift["id"] == self.shift_id:
                return shift
        ValueError(f"Shift with {self.shift_id} not found in payload")

    def _get_employee_from_payload(self):
        for employee in self.employees:
            if employee["id"] == self.user_id:
                return employee
        ValueError(f"Employee with {self.user_id} not found in payload")

    def _prepare_payload(self):
        shift = self._get_shift_from_payload()
        user = self._get_employee_from_payload()
        settings = self.settings
        settings["return_ineligibility_reasons"] = True

        return {
            "shifts": [shift],
            "users": [user],
            "rules": self.rules,  # or []
            "settings": settings,
        }

    def check_eligibility(self):
        payload = self._prepare_payload()
        result = self.run_payload(payload)
        return self._interpreter_payload(result)

    def run_payload(self, payload):
        return self.alfa.invoke_algorithm(payload)

    def _interpreter_payload(self, result):
        unassigned_shifts = result["unassigned_shifts"]  # always one?

        if len(unassigned_shifts) == 0:
            return [
                "There are no unassigned shifts."
            ]

        eligibility_reasons = unassigned_shifts[0].get("ineligibility_reasons", None)

        if eligibility_reasons is None:
            return [
                "There are no ineligibility reasons. "
                "If the shifts is not assigned, it is probably because of one of the rules."
            ]

        print(eligibility_reasons)
        return eligibility_reasons


if __name__ == "__main__":
    file = open('payload.json')
    payload = json.load(file)
    run_id = "c887d6ce-8c47-4682-b32b-e19f1f4d4f09"
    EligibilityChecker(run_id, 955678111, 2977987).check_eligibility()
