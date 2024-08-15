import time
import requests


class AlfaClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bearer_token = self.get_bearer_token()

    def _make_request(self, url, payload, method):
        if method == "POST":
            response = requests.post(
                url,
                json=payload,
                headers={
                    'wb-authorization': f'Bearer {self.bearer_token}'
                }
            )
        elif method == "GET":
            response = requests.get(
                url,
                json={
                    "returnReference": False
                },
                headers={
                    'wb-authorization': f'Bearer {self.bearer_token}'
                }
            )
        else:
            raise ValueError("Invalid method")

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Request failed with status code {response.status_code}")
        return data

    def invoke_algorithm(self, payload):
        url = "https://alfa-baas-eu-central-1.web.quinyx.com/api/Algorithms/submitRequest"
        data = {
            "algorithmId": "c8503cde-d0ff-431b-a99f-4a94895a6e7e",
            # should be user input? Or does not depend per team?
            "environment": "production",
            "problem": payload,
            "returnHoldingResponse": True,
            "returnReference": False,
            "runOptions": {},
        }
        response = self._make_request(url, data, "POST")
        run_id = response["id"]
        time.sleep(1)
        return self.poll_result(run_id)

    def poll_result(self, run_id):
        """function that should poll the result of the run until it is completed.
        Should stop polling after 3 retries.
        """
        retries = 0
        result = None
        url = f"https://alfa-baas-eu-central-1.web.quinyx.com/api/AlgorithmRuns/{run_id}/response"
        while retries < 3:
            run_output = self._make_request(url, {}, "GET")
            if run_output != "":
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
        url = f"https://alfa-baas-eu-central-1.web.quinyx.com/api/AlgorithmRuns/{run_id}"
        while retries < 3:
            run_output = self._make_request(url, {}, "GET")
            if run_output != "":
                result = run_output
                break
            time.sleep(2)
            retries += 1

        return result["problem"]

    def get_bearer_token(self):
        url = "https://alfa-baas-eu-central-1.web.quinyx.com/requestToken"
        payload = f'{{"clientId":"{self.client_id}", "clientSecret": "{self.client_secret}"}}'
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        respone_data = response.json()
        return respone_data["access_token"]

def request_oauth_token(url_core, client_id, client_secret):
    url = url_core + "/api/ApiKeyValidators/requestToken"

    res = requests.post(
        url,
        data={
            "clientId": client_id,
            "clientSecret": client_secret,
            "audience": url_core,
        },
    )
    res = res.json()

    if "error" in res:
        raise ValueError("Failed to get token")

    token = res["token_type"] + " " + res["access_token"]
    return token
