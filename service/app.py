# coding=utf-8
import requests
from apig_sdk import signer

if __name__ == '__main__':
    sig = signer.Signer()
    # Set the AK/SK to sign and authenticate the request.
    sig.Key = "LWYFNIIRUKPRQUYSBZPY"
    sig.Secret = "NNv1sCj6ufH4h82Q9fQCoLl6JDeUfEYdvFkOHqo0"

		# url = "https://e34e30bda81f4586a03250b37a863d36.infer.xckpjs.com/v1/infers/d8250d26-6a42-40ba-9454-0ff93119576b"
		# ak = "LWYFNIIRUKPRQUYSBZPY"
		# sk = "NNv1sCj6ufH4h82Q9fQCoLl6JDeUfEYdvFkOHqo0"
    # The following example shows how to set the request URL and parameters to query a VPC list.
    # Set request Endpoint.
    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    # Set request URI.
    # Set parameters for the request URL.
    r = signer.HttpRequest("GET", "https://e34e30bda81f4586a03250b37a863d36.infer.xckpjs.com/v1/infers/d8250d26-6a42-40ba-9454-0ff93119576b")

    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = ""
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])

    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)
    print(resp.status_code, resp.reason)
    print(resp.content)
