import os
import threading
from flask import Flask, render_template_string, request
from git import Repo, InvalidGitRepositoryError
from pathlib import Path
import shutil

# --- Carpetas principales ---
BASE_DIR = Path(__file__).parent.resolve()
REPOS_DIR = BASE_DIR / "repos"
OUTPUTS_DIR = BASE_DIR / "outputs"
VIDEOS_DIR = BASE_DIR / "videos"
PROJECTS_DIR = BASE_DIR / "projects"

for folder in [REPOS_DIR, OUTPUTS_DIR, VIDEOS_DIR, PROJECTS_DIR]:
    folder.mkdir(exist_ok=True)

# --- Flask App ---
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Sofía 4.7 Multiagente</title>
<style>
body { font-family: Arial; margin: 30px; background:#f0f0f0; }
input, textarea, button { width:100%; padding:10px; margin:5px 0; }
textarea { height:80px; }
.output { background:#fff; padding:15px; margin-top:20px; border-radius:5px; box-shadow:0 0 5px #aaa; white-space: pre-wrap; }
</style>
</head>
<body>
<h1>Sofía 4.7 - Multiagente Web</h1>
<form method="POST" action="/process">
<label>Prompt para Sofía:</label>
<textarea name="prompt"></textarea>
<button type="submit">Ejecutar</button>
</form>

<h2>Repositorios gestionados</h2>
<ul>
{% for repo in repos %}
<li>{{ repo.name }} - <a href="/download/{{ repo.name }}">Informe</a></li>
{% endfor %}
</ul>

<div class="output">
<h3>Salida:</h3>
<pre>{{ output }}</pre>
</div>
</body>
</html>
"""

# --- Funciones Multiagente ---
def safe_mkdir(path: Path):
    path.mkdir(exist_ok=True)

def clone_repo(url):
    repo_name = url.rstrip("/").split("/")[-1]
    target_path = REPOS_DIR / repo_name
    if target_path.exists():
        try:
            Repo(target_path)
            return f"[SKIP] Repo ya válido: {repo_name}"
        except InvalidGitRepositoryError:
            shutil.rmtree(target_path)
    Repo.clone_from(url, target_path)
    return f"[OK] Repo clonado: {repo_name}"

def analyze_repo(repo_name):
    output_file = OUTPUTS_DIR / f"{repo_name}_report.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"[ANALYZE] Analizando repo: {repo_name}\n")
        f.write("Resultado simulado de análisis y generación de contenido.\n")
        f.write("Contenido listo para plataformas legales.\n")
    return f"[REPORT] Guardado en: {output_file}"

def process_prompt_multi(prompt):
    result = f"[Sofía4.7] Prompt recibido: {prompt}\n"
    result += "[INFO] Procesando repos y proyectos en paralelo...\n"
    
    # Ejemplo de multiagente: clones y análisis en hilos
    repo_urls = [
        "https://github.com/octocat/Hello-World.git",
        "https://github.com/octocat/Spoon-Knife.git",
        "https://github.com/octocat/test-repo1.git"
    ]
    
    threads = []
    repo_results = []

    def agent_task(url):
        msg_clone = clone_repo(url)
        repo_name = url.rstrip("/").split("/")[-1]
        msg_analyze = analyze_repo(repo_name)
        repo_results.append(msg_clone + "\n" + msg_analyze)
    
    for url in repo_urls:
        t = threading.Thread(target=agent_task, args=(url,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    for r in repo_results:
        result += r + "\n"

    # Crear proyecto de contenido simulado
    project_name = f"SofiaProject_{len(list(PROJECTS_DIR.iterdir())) + 1}"
    project_path = PROJECTS_DIR / project_name
    safe_mkdir(project_path)
    readme_file = project_path / "README.txt"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(f"Proyecto: {project_name}\nPrompt: {prompt}\n")
        f.write("Contenido generado listo para plataformas legales.\n")
    result += f"[APP] Proyecto creado en: {project_path}\n"
    
    return result

# --- Rutas web ---
@app.route("/", methods=["GET"])
def index():
    repos = [r for r in REPOS_DIR.iterdir() if r.is_dir()]
    return render_template_string(HTML_TEMPLATE, repos=repos, output="Bienvenida a Sofía 4.7 Multiagente")

@app.route("/process", methods=["POST"])
def process():
    prompt = request.form.get("prompt", "")
    output = process_prompt_multi(prompt)
    repos = [r for r in REPOS_DIR.iterdir() if r.is_dir()]
    return render_template_string(HTML_TEMPLATE, repos=repos, output=output)

@app.route("/download/<repo_name>", methods=["GET"])
def download_report(repo_name):
    file_path = OUTPUTS_DIR / f"{repo_name}_report.txt"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    return "Archivo no encontrado."

# --- Ejecutar servidor ---
if __name__ == "__main__":
    print("✅ Sofía 4.7 Multiagente iniciada. Abre tu navegador en http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
