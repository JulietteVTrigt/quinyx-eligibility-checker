from alfa_sdk.common.session import Session
import time


def alfa_run(payload, client_id, client_secret):
    print(client_id, client_secret)
    alfa_session = Session(
        credentials={
            "clientId": client_id,  # "c21c1bd2-fc1d-4ad5-9bec-34068388989d",
            "clientSecret": client_secret # "Phd_dVmRIYJ-qqrI70UH-AW87jXdDFCa7NCfXCDnwbqYfktdLYVssjGBqAj1Cpuv",
        }
    )
    # works because of variables stored in config should - be user input

    response = (
        alfa_session.request(
            service="baas",
            path="/api/Algorithms/submitRequest",
            method="POST",
            json={
                "algorithmId": "c8503cde-d0ff-431b-a99f-4a94895a6e7e",  # should be user input? Or does not depend per team?
                "environment": "production",
                "problem": payload,
                "returnHoldingResponse": True,
                "returnReference": False,
                "runOptions": {}
            }
        )
    )

    run_id = response["id"]
    time.sleep(1)

    # Fetch run status / result
    run_output = (
        alfa_session.request(
            service="baas",
            path=f"/api/AlgorithmRuns/{run_id}/response",
            method="GET"
        )
    )
    print(run_output)
    return run_output


if __name__ == "__main__":
    payload = {
        "users": [],
        "shifts": [],
        "rules": [],
        "settings": {
            "start": 0,
            "finish": 1
        }
    }
    alfa_run(payload)
