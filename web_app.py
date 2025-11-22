import os
import threading
from typing import List

from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string, abort

try:
    from CodeSmellTool import file_extractor
except Exception:
    file_extractor = None

from src.detector import detect_main
from src.config_loader import get_config
from tools.report_html import generate_html_report


app = Flask(__name__)


def _safe_basename(path: str) -> str:
    try:
        return os.path.basename(os.path.normpath(path))
    except Exception:
        return "project"


def _list_plots() -> List[str]:
    plots_dir = get_config().get_plots_dir()
    if not os.path.isdir(plots_dir):
        return []
    files = []
    for name in sorted(os.listdir(plots_dir)):
        if name.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            files.append(name)
    return files


@app.route("/")
def index():
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>CodeSmellTool Web</title>
        <style>
            body {font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif; margin:0; background:#f5f7fb;}
            .wrap {max-width: 960px; margin: 40px auto; background:#fff; border-radius:12px; box-shadow:0 6px 24px rgba(0,0,0,0.08);}
            header {padding: 24px 32px; border-bottom: 1px solid #eee;}
            header h1 {margin:0; font-size: 22px;}
            .content {padding: 24px 32px;}
            label {display:block; font-weight:600; margin: 16px 0 8px;}
            input[type=text] {width:100%; padding:12px 14px; border:1px solid #cfd8dc; border-radius:8px;}
            .row {display:flex; gap:12px;}
            .btn {display:inline-block; padding:10px 16px; border-radius:8px; border:none; cursor:pointer; font-weight:600;}
            .btn-primary {background:#2667ff; color:#fff;}
            .btn-secondary {background:#e8eef5; color:#1f2d3d;}
            .card {margin-top:20px; padding:16px; border:1px solid #eee; border-radius:10px;}
            .footer {padding: 16px 32px; color:#7a8793; font-size: 12px;}
        </style>
    </head>
    <body>
        <div class="wrap">
            <header>
                <h1>Code Smell Tool</h1>
            </header>
            <div class="content">
                <form method="post" action="/run-upload" enctype="multipart/form-data">
                    <label>Select Project Directory (uploads all .py files inside)</label>
                    <input id="dirInput" type="file" name="files" webkitdirectory directory multiple required style="display:none;" onchange="document.getElementById('dirStatus').textContent='Directory selected'" />
                    <div class="row">
                        <button class="btn btn-secondary" type="button" onclick="document.getElementById('dirInput').click()">Select Directory</button>
                        <span id="dirStatus" style="align-self:center; color:#7a8793;">No directory selected</span>
                    </div>
                    <div class="row" style="margin-top:16px;">
                        <button class="btn btn-primary" type="submit">Run Detection</button>
                        <a class="btn btn-secondary" href="/gallery" target="_blank">View Historical Charts</a>
                    </div>
                </form>
                <div class="card">
                    <strong>Instructions</strong>
                    <ul>
                        <li>Select local directories via Edge/Chrome; no path typing required.</li>
                        <li>Detection generates an HTML report and charts, viewable in the browser.</li>
                        <li>Charts go to the configured `plots` directory; logs to `output/logs`.</li>
                    </ul>
                </div>
            </div>
        </div>
        
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/run-upload", methods=["POST"])
def run_upload():
    files = request.files.getlist('files')
    if not files:
        abort(400, description="No directory selected")

    # Parse the top-level directory name (from webkitRelativePath)
    top = None
    for f in files:
        p = f.filename.replace('\\', '/')
        if '/' in p:
            top = p.split('/')[0]
            break
    base = top or "uploaded_project"
    dump_dir = os.path.join("code-dump", base)
    os.makedirs(dump_dir, exist_ok=True)

    # Clear old files
    for entry in os.scandir(dump_dir):
        if entry.is_file():
            try:
                os.unlink(entry.path)
            except OSError:
                pass

    # Flat save the.py files
    idx = 0
    for f in files:
        name = f.filename
        if name.lower().endswith('.py'):
            target_name = f"{idx:04d}_{os.path.basename(name)}"
            dst = os.path.join(dump_dir, target_name)
            try:
                f.save(dst)
                idx += 1
            except Exception:
                continue

    # Run detection
    detect_main(dump_dir, None)

    # Generate HTML report and redirect
    generate_html_report(base)
    return redirect(url_for("reports_index", filename=f"{base}_review.html"))


@app.route("/view/<dirname>")
def view_report(dirname: str):
    # Change to directly generate and display HTML reports
    generate_html_report(dirname)
    return redirect(url_for("reports_index", filename=f"{dirname}_review.html"))


@app.route("/gallery")
def gallery():
    plots = _list_plots()
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Chart Gallery</title>
        <style>
            body {font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif; margin:0; background:#f5f7fb;}
            .wrap {max-width: 1100px; margin: 32px auto;}
            .panel {background:#fff; border-radius:12px; box-shadow:0 6px 24px rgba(0,0,0,0.08); padding:18px;}
            .grid {display:grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:16px;}
            .img-card {background:#fff; border:1px solid #eee; border-radius:10px; padding:10px;}
            .img-card img {max-width: 100%; height:auto; display:block;}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="panel">
                <h2>All Charts (plots directory)</h2>
                {% if plots %}
                <div class="grid">
                    {% for img in plots %}
                    <div class="img-card"><img src="{{ url_for('get_plot', filename=img) }}" alt="{{ img }}" /></div>
                    {% endfor %}
                </div>
                {% else %}
                <p>No charts available.</p>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, plots=plots)


@app.route("/reports/<path:filename>")
def get_report(filename: str):
    output_dir = get_config().get_output_dir()
    return send_from_directory(output_dir, filename)

@app.route("/reports")
def reports_index():
    # Redirect to the specified report file
    filename = request.args.get('filename')
    if not filename:
        abort(404)
    return redirect(url_for('get_report', filename=filename))


@app.route("/plots/<path:filename>")
def get_plot(filename: str):
    plots_dir = get_config().get_plots_dir()
    return send_from_directory(plots_dir, filename)


if __name__ == "__main__":
    # Run in production mode and disable automatic reloading to avoid watchdog version compatibility issues
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)