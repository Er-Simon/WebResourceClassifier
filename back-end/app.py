from flask import Flask, request
from flask_cors import CORS

from json import loads
from website_classification import classify

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.post("/")
def handle_request():
    request_data = None
    response = "INTERNAL ERROR"

    if request.data:
        request_data = loads(request.data)

        if "title" in request_data and "description" in request_data:
            response = classify(request_data["title"], request_data["description"])

    print("[INFO] response: {}".format(response))
    return response

if __name__ == "__main__":
    app.run()