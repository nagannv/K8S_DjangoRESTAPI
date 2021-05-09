import requests


def api_post(api, req_body):
    response = requests.post(api, json=req_body)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Failed to post the request")


def api_delete(api, body):
    del_response = requests.delete(api, json=body)
    if del_response.status_code == 200:
        return del_response.content
    else:
        raise Exception("Failed to do a delete request")