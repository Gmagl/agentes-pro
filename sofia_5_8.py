import os
import subprocess
import signal
import socket
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

app = Flask(__name__)

# =============================
# CONFIG
# =============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
REPOS_FILE = os.path.join(BASE_DIR, "repos.txt")

os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

running_apps = {}

# =============================
# UTILS
# =============================

def get_free_port():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def detectar_app_ejecutable(path):
    for f in ["app.py", "main.py", "run.py"]:
        if os.path.exists(os.path.join(path, f)):
            return f
    return None


def listar_repos():
    if not os.path.exists(REPOS_FILE):
        return []
    with open(REPOS_FILE, "r", encoding="utf-8") as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def guardar_repo(url):
    repos = listar_repos()
    if url not in repos:
        with open(REPOS_FILE, "a", encoding="utf-8") as f:
            f.write(url + "\n")

# =============================
# DASHBOARD
# =============================

@app.route("/")
def dashboard():
    proyectos = os.listdir(PROJECTS_DIR)
    videos = os.listdir(VIDEOS_DIR)
    repos = listar_repos()

    return render_template(
        "dashboard_5_8.html",
        proyectos=proyectos,
        videos=videos,
        repos=repos,
        running_apps=running_apps
    )

# =============================
# VIDEOS (FIX ERROR)
# =============================

@app.route("/video/<filename>")
def get_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)


@app.route("/procesar_video", methods=["POST"])
def procesar_video():
    file = request.files.get("video")
    if file:
        path = os.path.join(VIDEOS_DIR, file.filename)
        file.save(path)
    return redirect(url_for("dashboard"))

# =============================
# SPACES MODE (MULTI APP)
# =============================

@app.route("/spaces_run/<name>")
def spaces_run(name):
    path = os.path.join(PROJECTS_DIR, name)
    archivo = detectar_app_ejecutable(path)

    if not archivo:
        return redirect(url_for("dashboard"))

    if name in running_apps:
        return redirect(url_for("dashboard"))

    port = get_free_port()

    try:
        proc = subprocess.Popen(
            ["python", archivo, str(port)],
            cwd=path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        running_apps[name] = {
            "pid": proc.pid,
            "port": port
        }

    except Exception as e:
        print("Error ejecutando:", e)

    return redirect(url_for("dashboard"))


@app.route("/spaces_stop/<name>")
def spaces_stop(name):
    info = running_apps.get(name)

    if info:
        try:
            os.kill(info["pid"], signal.SIGTERM)
        except:
            pass
        running_apps.pop(name, None)

    return redirect(url_for("dashboard"))

# =============================
# AUTO DEPLOY HF (PREPARACIÓN)
# =============================

@app.route("/hf_prepare/<name>")
def hf_prepare(name):
    path = os.path.join(PROJECTS_DIR, name)

    readme = os.path.join(path, "README.md")
    requirements = os.path.join(path, "requirements.txt")

    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write(f"# {name}\nApp generada por Sofía\n")

    if not os.path.exists(requirements):
        with open(requirements, "w", encoding="utf-8") as f:
            f.write("flask\n")

    return redirect(url_for("dashboard"))

# =============================
# BORRAR PROYECTO
# =============================

@app.route("/delete_project/<name>")
def delete_project(name):
    path = os.path.join(PROJECTS_DIR, name)

    if os.path.exists(path):
        import shutil
        shutil.rmtree(path)

    running_apps.pop(name, None)
    return redirect(url_for("dashboard"))

# =============================
# CLONAR REPO
# =============================

@app.route("/clone_repo", methods=["POST"])
def clone_repo():
    url = request.form.get("repo_url")
    if not url:
        return redirect(url_for("dashboard"))

    nombre = url.split("/")[-1].replace(".git", "")
    destino = os.path.join(PROJECTS_DIR, nombre)

    if not os.path.exists(destino):
        subprocess.call(["git", "clone", url, destino])
        guardar_repo(url)

    return redirect(url_for("dashboard"))

# =============================
# RUN (ACCESO MÓVIL)
# =============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
