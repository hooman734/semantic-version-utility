from helpers.retrieve_v3 import resolve_version

from flask import Flask, render_template

app = Flask(__name__, template_folder="views")


@app.route('/')
def index():
    return render_template("index.jinja2")


@app.route('/api/nuget/<package_name>/<type>')
def next_version(package_name, type):
    major, minor, patch_prefix, patch = resolve_version(package_name)
    major, minor, patch = int(major), int(minor), int(patch)
    if major*minor*patch < 0:
        return render_template("404.jinja2", value = package_name)
    if type == 'major':
        major += 1
    if type == 'minor':
        minor += 1
    if type == 'patch':
        patch += 1
    if patch_prefix != '':
        patch = str(patch_prefix)+'.'+str(patch)

    return render_template("index.jinja2", value = (package_name, type, (str(major), str(minor), patch)))


if __name__ == '__main__':
    app.run(debug=True)
