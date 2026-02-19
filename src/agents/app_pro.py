import os
import threading
import shutil
from git import Repo, InvalidGitRepositoryError
from pathlib import Path
from yt_dlp import YoutubeDL
from flask import Flask, request, jsonify

# ---------------- CONFIG ----------------
REPOS_DIR = Path("repos")
OUTPUTS_DIR = Path("outputs")
VIDEOS_DIR = Path("videos")
PROJECTS_DIR = Path("projects/Sofia2026_v4")
AGENTS = ["Sofía4.0"]
FLASK_PORT = 5000

# ---------------- UTILIDADES ----------------
def safe_mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def clone_repo(url: str) -> Path:
    repo_name = url.rstrip("/").split("/")[-1]
    target_path = REPOS_DIR / repo_name
    if target_path.exists():
        print(f"[SKIP] Repo ya válido: {repo_name}")
        return target_path
    print(f"[INFO] Clonando: {url}")
    try:
        Repo.clone_from(url, target_path)
    except Exception as e:
        print(f"[ERROR] Fallo al clonar {url}: {e}")
    else:
        print(f"[OK] Repo clonado en: {target_path}")
    return target_path

def analyze_repo(path: Path):
    print(f"[ANALYZE] Analizando repo: {path.name}")
    # Aquí va análisis de código, correcciones IA, resúmenes
    report_path = OUTPUTS_DIR / f"{path.name}_report.txt"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"Análisis automático del repo {path.name}\n")
        f.write("TODO: agregar análisis y correcciones de IA\n")
    print(f"[REPORT] Guardado en: {report_path}")

def download_video(url: str):
    safe_mkdir(VIDEOS_DIR)
    ydl_opts = {"outtmpl": str(VIDEOS_DIR / "%(title)s.%(ext)s")}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        print(f"[VIDEO] Descargado en: {VIDEOS_DIR}")
        return info

def create_app_template(app_name: str):
    safe_mkdir(PROJECTS_DIR)
    app_path = PROJECTS_DIR / app_name
    safe_mkdir(app_path)
    readme = app_path / "README.txt"
    with readme.open("w", encoding="utf-8") as f:
        f.write(f"Plantilla app generada por Sofía4.0: {app_name}\n")
        f.write("Contiene instrucciones, scripts y plantillas listas para usar.\n")
    print(f"[APP] Creada plantilla app: {app_name} en {app_path}")
    return app_path

# ---------------- AGENTE ----------------
def agent_task():
    safe_mkdir(REPOS_DIR)
    safe_mkdir(OUTPUTS_DIR)
    
    # Lista de repos de ejemplo, puede venir de input
    repos_to_clone = [
        "https://github.com/octocat/Hello-World.git",
        "https://github.com/octocat/Spoon-Knife.git",
        "https://github.com/octocat/test-repo1.git"
    ]
    
    # Clonar y analizar
    for url in repos_to_clone:
        repo_path = clone_repo(url)
        analyze_repo(repo_path)
    
    # Descargar ejemplo de video
    download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    # Crear plantilla app
    create_app_template("SofiaApp_v4_0")

# ---------------- FLASK WEB ----------------
app = Flask(__name__)

@app.route("/prompt", methods=["POST"])
def handle_prompt():
    data = request.json
    prompt = data.get("prompt", "")
    # Aquí podrías integrar IA real para generar respuesta
    response = f"[Sofía4.0] Recibido tu prompt: {prompt}\n" \
               f"TODO: analizar, generar apps, scripts, videos según el prompt."
    return jsonify({"response": response})

# ---------------- MAIN ----------------
def main():
    print(f"[START] Agente {AGENTS[0]} iniciado.")
    
    # Hilo del agente principal
    t = threading.Thread(target=agent_task)
    t.start()
    t.join()
    
    print(f"✅ TODO TERMINADO por {AGENTS[0]}")
    print(f"[INFO] Revisa las carpetas: {REPOS_DIR}, {OUTPUTS_DIR}, {VIDEOS_DIR}, {PROJECTS_DIR}")
    print(f"[INFO] Para usar la interfaz web, abre http://localhost:{FLASK_PORT} y envía POST a /prompt")

if __name__ == "__main__":
    # Ejecutar agente principal
    main()
    # Ejecutar servidor web opcional
    app.run(port=FLASK_PORT)
