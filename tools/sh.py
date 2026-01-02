import subprocess,os,platform

_win=platform.system()=='Windows'

def run(cmd,cwd=None,timeout=60,shell=True):
    cwd=cwd or os.getcwd()
    try:
        r=subprocess.run(cmd,shell=shell,cwd=cwd,capture_output=True,text=True,timeout=timeout)
        return {'ok':r.returncode==0,'code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    except subprocess.TimeoutExpired:
        return {'ok':False,'code':-1,'stdout':'','stderr':f'timeout {timeout}s'}
    except Exception as e:
        return {'ok':False,'code':-1,'stdout':'','stderr':str(e)}

def run_bg(cmd,cwd=None):
    cwd=cwd or os.getcwd()
    try:
        if _win:
            p=subprocess.Popen(cmd,shell=True,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            p=subprocess.Popen(cmd,shell=True,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        return p
    except:return None

def check_cmd(name):
    chk='where' if _win else 'which'
    return run(f"{chk} {name}")['ok']

def get_shell():
    if _win:return os.environ.get('COMSPEC','cmd.exe')
    return os.environ.get('SHELL','/bin/bash')

def kill_proc(p):
    if p:
        try:p.terminate();p.wait(timeout=5)
        except:p.kill()
