<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sofía 5.8 – Dashboard Web</title>
<style>
body{font-family:Arial;margin:20px;background:#f0f0f5;}
h1{color:#222;} 
.section{margin-bottom:30px;background:#fff;padding:15px;border-radius:10px;box-shadow:0 0 15px #ccc;}
input[type=text]{width:300px;padding:5px;margin-right:5px;} 
select{padding:5px;margin-right:5px;} 
button{padding:5px 10px;margin-right:5px;} 
.msg{color:green;font-weight:bold;margin-top:10px;}
ul{list-style:none;padding:0;}
li{margin:5px 0;}
</style>
</head>
<body>
<h1>Sofía 5.8 – Dashboard Web</h1>
<div class="msg">{{ msg }}</div>

<div class="section">
<h2>Repositorios</h2>
<form method="post">
<input type="text" name="target" placeholder="GitHub URL o nombre repo">
<button type="submit" name="action" value="clone_repo">Clonar Repo</button>
<button type="submit" name="action" value="analyze_repo">Analizar Informe</button>
</form>
<ul>{% for r in repos %}<li>{{ r }}</li>{% endfor %}</ul>
</div>

<div class="section">
<h2>Proyectos / Apps</h2>
<form method="post">
<input type="text" name="target" placeholder="Nombre App">
<select name="style">
<option value="default">Default</option>
<option value="elegant">Elegante</option>
<option value="minimal">Minimalista</option>
<option value="moderno">Moderno</option>
<option value="fantasia">Fantasia</option>
</select>
<button type="submit" name="action" value="create_app">Crear App + Flow n8n</button>
</form>
<ul>{% for p in projects %}<li>{{ p }}</li>{% endfor %}</ul>
</div>

<div class="section">
<h2>Videos / Multimedia</h2>
<form method="post" enctype="multipart/form-data">
<input type="text" name="target" placeholder="Path video o URL">
<button type="submit" name="action" value="process_video">Procesar Video</button>
</form>
<ul>{% for v in videos %}<li><a href="{{ url_for('get_video',filename=v) }}">{{ v }}</a></li>{% endfor %}</ul>
</div>

<div class="section">
<h2>Generar Contenido Social Legal</h2>
<form method="post">
<input type="text" name="target" placeholder="Prompt natural">
<select name="style">
<option value="default">Default</option>
<option value="elegant">Elegante</option>
<option value="minimal">Minimalista</option>
<option value="moderno">Moderno</option>
<option value="fantasia">Fantasia</option>
</select>
<button type="submit" name="action" value="generate_social">Generar Contenido</button>
</form>
<ul>{% for s in social %}<li><a href="{{ url_for('get_social',filename=s) }}">{{ s }}</a></li>{% endfor %}</ul>
</div>

<div class="section">
<h2>Flujos n8n</h2>
<ul>{% for f in flows %}<li><a href="{{ url_for('get_flow',filename=f) }}">{{ f }}</a></li>{% endfor %}</ul>
</div>
</body>
</html>
