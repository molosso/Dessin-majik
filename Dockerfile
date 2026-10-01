FROM python:3.10-slim

# Installer les dépendances système nécessaires pour OpenCV (GUI/Mesa) et Tkinter
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .

# Variable d'environnement pour l'affichage graphique
ENV DISPLAY=:0

CMD ["python", "app.py"]