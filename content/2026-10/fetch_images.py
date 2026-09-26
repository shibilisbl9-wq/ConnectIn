"""Download the Higgsfield images, cut out the models, then rebuild slides and PSDs.

Needs d8j0ntlcm91z4.cloudfront.net to be reachable. Without it, download each file from your
Higgsfield library, save it under images/ with the name below (models as <name>-raw.png), and run
this script with --local to skip the download step.

Cut-outs use rembg's u2net_human_seg model locally (free, no Higgsfield credits):
    pip install "rembg[cpu]" psd-tools
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'images')
BASE = 'https://d8j0ntlcm91z4.cloudfront.net/user_30oPqzHbQR8C0wTVUe5fsO7jmVX/'
PHOTOS = {
    'img-1-skyline.png': 'hf_20260925_161440_7e11b0f8-3623-41fb-b6c8-d00a19c27a6b.png',
    'img-2-fork.png': 'hf_20260925_161439_0c6a98d4-9e9b-48ac-a38f-cc38d4063ba3.png',
    'img-3-bank.png': 'hf_20260925_161439_43535652-991a-4dc0-a78b-704e981c6d82.png',
    'img-4-scale.png': 'hf_20260925_161441_6ea14b77-2283-451d-a2bd-6954b68b639b.png',
    'img-5-tower.png': 'hf_20260925_161438_ffedbe98-745e-4cb1-94cb-df41e191695c.png',
}
MODELS = {
    'model-1-businessman.png': 'hf_20260926_002527_94e10a80-8c62-4b6e-951a-cf98d3d6aa83.png',
    'model-2-emirati.png': 'hf_20260926_002527_5adb758c-e65a-48aa-a418-33eb0bc4e4bc.png',
    'model-3-consultant.png': 'hf_20260926_002527_dd5a2ad8-62c3-43b8-b804-6be15f851381.png',
}


def download():
    failed = []
    for name, remote in list(PHOTOS.items()) + [(n.replace('.png', '-raw.png'), r) for n, r in MODELS.items()]:
        if subprocess.run(['curl', '-fsS', '-o', os.path.join(IMG, name), BASE + remote]).returncode:
            failed.append(name)
    if failed:
        sys.exit('Could not download: ' + ', '.join(failed))


def cut_out():
    from PIL import Image
    from rembg import new_session, remove
    session = new_session('u2net_human_seg')
    for name in MODELS:
        raw = Image.open(os.path.join(IMG, name.replace('.png', '-raw.png'))).convert('RGB')
        cut = remove(raw, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240,
                     alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
        cut = cut.crop(cut.getbbox())  # trim to the figure so the layout can scale it by height
        cut.save(os.path.join(IMG, name))
        print('cut out', name, cut.size)


def run(*cmd):
    env = dict(os.environ, NODE_PATH=subprocess.check_output(['npm', 'root', '-g'], text=True).strip())
    subprocess.run(cmd, check=True, cwd=HERE, env=env)


if __name__ == '__main__':
    os.makedirs(IMG, exist_ok=True)
    if '--local' not in sys.argv:
        download()
    cut_out()
    run(sys.executable, 'build.py')
    run('node', 'render.js')
    run('node', 'psd_layers.js')
    run(sys.executable, 'make_psd.py')
