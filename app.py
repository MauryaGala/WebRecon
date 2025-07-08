from flask import Flask, render_template, request, send_file
import subprocess
import sys
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target = request.form.get("target", "").strip()
        if not target:
            return render_template("index.html", error="Please enter a domain or IP address.")

        try:
            # Use the same Python that's running Flask
            python_path = sys.executable

            # Run the scan command
            result = subprocess.run(
                [python_path, "webrecon.py", target],
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout

            # Look for JSON file
            safe_target = target.replace("/", "_").replace("\\", "_").replace(":", "_")
            json_file = f"{safe_target}_scan_results.json"

            return render_template("results.html", output=output, json_file=json_file)

        except subprocess.CalledProcessError as e:
            error_output = e.stderr or "An error occurred during scanning."
            return render_template("results.html", output=error_output)
        except Exception as e:
            return render_template("results.html", output=f"Unexpected error: {str(e)}")

    return render_template("index.html")


@app.route("/download/<filename>")
def download_json(filename):
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404


# Optional: Debug route to show Python environment info
@app.route("/env")
def check_env():
    import sys
    env_info = f"<h2>Python Executable:</h2> <p>{sys.executable}</p><br>"
    env_info += "<h2>Sys Path:</h2><ul>"
    for path in sys.path:
        env_info += f"<li>{path}</li>"
    env_info += "</ul>"
    return env_info



@app.route("/cwd")
def check_cwd():
    return f"<h2>Current Working Directory:</h2> <p>{os.getcwd()}</p>"


if __name__ == "__main__":
    app.run(debug=True)