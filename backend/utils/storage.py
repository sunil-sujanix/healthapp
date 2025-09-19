import os, uuid
from flask import current_app, abort

def ensure_upload_dir():
    updir = os.path.abspath("uploads")
    os.makedirs(updir, exist_ok=True)
    return updir

def save_file(fileobj, filename: str):
    updir = ensure_upload_dir()
    ext = ""
    if "." in filename:
        ext = "." + filename.rsplit(".", 1)[1]
    key = f"docs_{uuid.uuid4().hex}{ext}"
    path = os.path.join(updir, key)

    fileobj.save(path)   # save the uploaded file
    return key, path

def get_file_path(key: str):
    path = os.path.join("uploads", key)
    if not os.path.isfile(path):
        abort(404)
    return path
