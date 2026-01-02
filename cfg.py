import os,json
from pathlib import Path

home_dir = Path.home()/'.codra'
home_dir.mkdir(exist_ok=True)

MODEL = 'llama3.2'
OLLAMA_URL = os.environ.get('OLLAMA_HOST','http://localhost:11434')

sess_path = home_dir/'sessions'
sess_path.mkdir(exist_ok=True)

cfgfile = home_dir/'config.json'

def _read():
    if cfgfile.exists():
        with open(cfgfile) as f: return json.load(f)
    return {}

def _write(d):
    with open(cfgfile,'w') as f: json.dump(d,f,indent=2)

def get_model():
    c=_read()
    return c.get('model',MODEL)

def set_model(m):
    c=_read()
    c['model']=m
    _write(c)

session_dir = sess_path
ollama_host = OLLAMA_URL
default_model = MODEL
