from alfa_sdk.common.session import Session
import time


class AlfaClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.alfa_session = self._initialize()

    def _initialize(self):
        return Session(
            credentials={
                "SESSIONID": "..."  # TODO - get from config?
            }
        )

    def invoke_algorithm(self, payload):
        response = (
            self.alfa_session.request(
                service="baas",
                path="/api/Algorithms/submitRequest",
                method="POST",
                json={
                    "algorithmId": "c8503cde-d0ff-431b-a99f-4a94895a6e7e",
                    # should be user input? Or does not depend per team?
                    "environment": "production",
                    "problem": payload,
                    "returnHoldingResponse": True,
                    "returnReference": False,
                    "runOptions": {}
                }
            )
        )
        run_id = response["id"]
        return self.poll_result(run_id)

    def poll_result(self, run_id):
        """function that should poll the result of the run until it is completed.
        Should stop polling after 3 retries.
        """
        retries = 0
        result = None
        while retries < 3:
            run_output = (
                self.alfa_session.request(
                    service="baas",
                    path=f"/api/AlgorithmRuns/{run_id}/response",
                    method="GET"
                )
            )
            if run_output is not "":
                result = run_output
                break
            time.sleep(2)
            retries += 1

        return result

    def poll_problem(self, run_id):
        """function that should poll the result of the run until it is completed.
        Should stop polling after 3 retries.
        """
        retries = 0
        result = None
        while retries < 3:
            run_output = (
                self.alfa_session.request(
                    service="baas",
                    path=f"/api/AlgorithmRuns/{run_id}",
                    method="GET"
                )
            )
            if run_output is not "":
                result = run_output
                break
            time.sleep(2)
            retries += 1

        return result["problem"]