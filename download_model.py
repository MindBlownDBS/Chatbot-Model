import os
from huggingface_hub import snapshot_download

model_dir = "./qwen-1.5-1.8B-local"

if os.path.isdir(model_dir) and os.listdir(model_dir):
    print(f"Model directory '{model_dir}' sudah ada dan tidak kosong. Skip download.")
else:
    print(f"Model directory '{model_dir}' belum ada atau kosong. Mulai download model...")
    snapshot_download(
        repo_id="Qwen/Qwen1.5-1.8B-Chat",
        local_dir=model_dir,
        local_dir_use_symlinks=False,
    )
    print("Download selesai.")
    