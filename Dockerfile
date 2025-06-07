# Gunakan image dasar Python
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu agar cache build efisien
COPY requirements.txt .

# Install system dependencies (kalau butuh git, bisa ditambahkan)
RUN apt-get update && apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Install semua Python dependencies dari requirements.txt
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Salin semua source code ke dalam container
COPY . .

# Download base model lokal
RUN python download_model.py

EXPOSE 8000

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
