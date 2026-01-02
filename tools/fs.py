import os
from pathlib import Path

def read_file(path):
    p=Path(path)
    if not p.exists():return None,f"not found: {path}"
    try:return p.read_text(encoding='utf-8'),None
    except Exception as e:return None,str(e)

def write_file(path,content):
    p=Path(path)
    try:
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content,encoding='utf-8')
        return True,None
    except Exception as e:return False,str(e)

def append_file(path,content):
    p=Path(path)
    try:
        p.parent.mkdir(parents=True,exist_ok=True)
        with open(p,'a',encoding='utf-8') as f:f.write(content)
        return True,None
    except Exception as e:return False,str(e)

def delete_file(path):
    p=Path(path)
    if not p.exists():return False,"not found"
    try:p.unlink();return True,None
    except Exception as e:return False,str(e)

def list_dir(path):
    p=Path(path)
    if not p.exists():return None,"dir not found"
    if not p.is_dir():return None,"not a dir"
    try:
        items=[]
        for i in p.iterdir():
            items.append({'name':i.name,'is_dir':i.is_dir(),'size':i.stat().st_size if i.is_file() else 0})
        return items,None
    except Exception as e:return None,str(e)

def make_dir(path):
    try:Path(path).mkdir(parents=True,exist_ok=True);return True,None
    except Exception as e:return False,str(e)

def file_exists(path):return Path(path).exists()
def get_cwd():return os.getcwd()

def tree(path,maxd=3,d=0):
    p=Path(path)
    if not p.exists():return ""
    indent="  "*d
    if p.is_file():return f"{indent}{p.name}"
    lines=[f"{indent}{p.name}/"]
    if d<maxd:
        try:
            for item in sorted(p.iterdir()):
                if item.name.startswith('.'):continue
                lines.append(tree(item,maxd,d+1))
        except:lines.append(f"{indent}  [denied]")
    return '\n'.join(lines)
