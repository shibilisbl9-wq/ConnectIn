"""Download the Higgsfield images into images/, then rebuild and re-render.

Needs d8j0ntlcm91z4.cloudfront.net to be reachable. Without it, download each image from your
Higgsfield library and save it under images/ with the file name listed below, then run:
    python3 build.py && NODE_PATH=$(npm root -g) node render.js
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://d8j0ntlcm91z4.cloudfront.net/user_30oPqzHbQR8C0wTVUe5fsO7jmVX/'
FILES = {
    'img-1-skyline.png': 'hf_20260925_161440_7e11b0f8-3623-41fb-b6c8-d00a19c27a6b.png',
    'img-2-fork.png': 'hf_20260925_161439_0c6a98d4-9e9b-48ac-a38f-cc38d4063ba3.png',
    'img-3-bank.png': 'hf_20260925_161439_43535652-991a-4dc0-a78b-704e981c6d82.png',
    'img-4-scale.png': 'hf_20260925_161441_6ea14b77-2283-451d-a2bd-6954b68b639b.png',
    'img-5-tower.png': 'hf_20260925_161438_ffedbe98-745e-4cb1-94cb-df41e191695c.png',
}

failed = []
for name, remote in FILES.items():
    out = os.path.join(HERE, 'images', name)
    r = subprocess.run(['curl', '-fsS', '-o', out, BASE + remote])
    if r.returncode:
        failed.append(name)
if failed:
    sys.exit('Could not download: ' + ', '.join(failed))
subprocess.run([sys.executable, os.path.join(HERE, 'build.py')], check=True)
subprocess.run(['node', os.path.join(HERE, 'render.js')], check=True,
               env=dict(os.environ, NODE_PATH=subprocess.check_output(['npm', 'root', '-g'], text=True).strip()))
