from flask import Flask, request, Response, redirect, render_template_string, abort
import requests
import yaml
from urllib.parse import urljoin
import werkzeug.exceptions

app = Flask(__name__)


# Load configuration from YAML file
def load_config():
    with open("proxy_config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


# Get target URL based on request path
def get_target_url(path, config):
    for rule in config["routes"]:
        if path.startswith(rule["path"]):
            stripped_path = path[len(rule["path"]) :]  # Strip the prefix from the path
            return rule["destination"], stripped_path
    return None, None


# Proxy request to the target URL
def proxy_request(target_url, path, method, headers, data):
    url = target_url[0] + "/" + target_url[1]
    print(url)
    response = requests.request(method, url, headers=headers, data=data)
    return response.content, response.status_code, response.headers


config = load_config()


@app.errorhandler(werkzeug.exceptions.HTTPException)
def error_page(e: werkzeug.exceptions.HTTPException):
    for error in config["errors"]:
        if e.code == error["status_code"]:
            return render_template_string(open(error["page"]).read(), error=e)


# Main proxy route
@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    config = load_config()
    target_url = get_target_url(path, config)
    print(target_url)
    if target_url is (None, None):
        abort(404)

    method = request.method
    headers = request.headers
    data = request.get_data()

    response_content, status_code, response_headers = proxy_request(
        target_url, path, method, headers, data
    )
    print(response_headers)
    # Check if the backend app sends a redirect
    if status_code in {301, 302, 303, 307, 308} and "Location" in response_headers:
        # Adjust the relative redirect URL based on the original request path
        original_url = request.base_url
        new_location = urljoin(original_url, response_headers["Location"])
        print(new_location)
        return redirect(new_location, status_code)

    headers = [(k, v) for k, v in response_headers.items()]
    r = Response(response_content, status_code, headers)
    return r


if __name__ == "__main__":
    app.run("0.0.0.0", 80)
