import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 📁 carpeta donde guardas tus proyectos
PROJECTS_DIR = "./proyectos"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/repos")
def list_repos():
    repos = []

    if os.path.exists(PROJECTS_DIR):
        for name in os.listdir(PROJECTS_DIR):
            path = os.path.join(PROJECTS_DIR, name)
            if os.path.isdir(path):
                repos.append({
                    "name": name,
                    "run_url": f"/run/{name}"
                })

    return jsonify(repos)

@app.route("/run/<repo>")
def run_repo(repo):
    return f"🚀 Aquí lanzaríamos: {repo}"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
