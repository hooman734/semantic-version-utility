from helpers.retrieve_v3 import resolve_version
from flask import Flask, render_template
from flask_cors import CORS
import json

app = Flask(__name__, template_folder="views")
CORS(app)


@app.route("/api/v1/users")
def list_users():
    return "user example"


@app.route('/')
def index():
    return render_template("welcome.jinja2")


@app.route('/api/nuget/<package_name>/<type>')
def next_version(package_name, type):
    major, minor, patch_prefix, patch = resolve_version(package_name)
    major, minor, patch = int(major), int(minor), int(patch)
    if major * minor * patch < 0:
        return render_template("404.jinja2", value=package_name)
    if type == 'major':
        major += 1
    if type == 'minor':
        minor += 1
    if type == 'patch':
        patch += 1
    if patch_prefix != '':
        patch = str(patch_prefix) + '.' + str(patch)

    return render_template("index.jinja2", value=(package_name, type, (str(major), str(minor), patch)))

@app.route('/api/nuget/<package_name>/<type>/json')
def next_version_json(package_name, type):
    major, minor, patch_prefix, patch = resolve_version(package_name)
    major, minor, patch = int(major), int(minor), int(patch)
    if major * minor * patch < 0:
        res = (package_name, 'null', 'null')
        return json.dumps(res)
    if type == 'major':
        major += 1
    if type == 'minor':
        minor += 1
    if type == 'patch':
        patch += 1
    if patch_prefix != '':
        patch = str(patch_prefix) + '.' + str(patch)

    res = (package_name, type, (str(major), str(minor), str(patch)))
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=False)
