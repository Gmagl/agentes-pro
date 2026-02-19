# ==== Setup completo para tu proyecto de agentes ====

# 1️⃣ Activar entorno virtual
$env:VENV_PATH = ".\agentes\Scripts\Activate.ps1"
if (-Not (Test-Path $env:VENV_PATH)) {
    Write-Host "No se encontró el entorno virtual 'agentes'. Creando uno..."
    python -m venv agentes
}
Write-Host "Activando entorno virtual..."
& $env:VENV_PATH

# 2️⃣ Instalar todas las librerías necesarias
Write-Host "Instalando librerías necesarias..."
pip install --upgrade pip
pip install yt-dlp selenium==4.20.0 gitpython openai langchain-core==1.2.13 langchain-community==0.4.1 langchain-experimental==0.4.1 langsmith==0.7.4

# 3️⃣ Descargar ChromeDriver compatible con Chrome 145
$chromeDriverUrl = "https://storage.googleapis.com/chrome-for-testing-public/145.0.7632.76/win64/chromedriver-win64.zip"
$chromeDriverZip = ".\chromedriver.zip"
$chromeDriverFolder = ".\chromedriver"

if (-Not (Test-Path $chromeDriverFolder)) {
    Write-Host "Descargando ChromeDriver..."
    Invoke-WebRequest -Uri $chromeDriverUrl -OutFile $chromeDriverZip
    Expand-Archive $chromeDriverZip -DestinationPath $chromeDriverFolder
    Remove-Item $chromeDriverZip
}

# 4️⃣ Crear carpetas base para agentes y repos
$folders = @(".\repos", ".\logs", ".\data")
foreach ($f in $folders) {
    if (-Not (Test-Path $f)) { New-Item -ItemType Directory -Path $f }
}

Write-Host "`n✅ Configuración completada."
Write-Host "Tu entorno virtual está activo, las librerías instaladas y ChromeDriver listo en: $chromeDriverFolder"
Write-Host "Ejecuta tus agentes con: python app_pro.py"
