from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def serve_index():
    return send_from_directory(".", "cocosolis_bg_landing.html")

@app.route("/<path:path>")
def serve_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
