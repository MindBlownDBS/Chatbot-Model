from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Qwen/Qwen1.5-1.8B-Chat",
    local_dir="./qwen-1.5-1.8B-local",
    local_dir_use_symlinks=False,
)