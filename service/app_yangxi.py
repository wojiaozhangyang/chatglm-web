# coding=utf-8
import requests
import json
from apig_sdk import signer

if __name__ == '__main__':

    url="https://e34e30bda81f4586a03250b37a863d36.infer.xckpjs.com/v1/infers/d8250d26-6a42-40ba-9454-0ff93119576b"
    method = 'POST'

    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    body = {
    "prompt":"你好",
    "history":[],
    "max_length":2048,
    "top_p":"",
    "temperature":""
    }

    r = signer.HttpRequest(method, url, headers, json.dumps(body))
    sig = signer.Signer()
    # Set the AK/SK to sign and authenticate the request.
    sig.Key = "LWYFNIIRUKPRQUYSBZPY"
    sig.Secret = "NNv1sCj6ufH4h82Q9fQCoLl6JDeUfEYdvFkOHqo0"
    sig.Sign(r)
    print(r.headers["content-type"])
    print(r.headers["Authorization"])

    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)
    decoded_content = resp.content.decode('utf-8')
    print(decoded_content)
    print(resp.status_code, resp.reason)
    # print(resp.content)
