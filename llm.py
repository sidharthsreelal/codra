import json,urllib.request,urllib.error
from cfg import ollama_host,get_model

def chat(msgs,model=None,stream=False):
    model=model or get_model()
    url=f"{ollama_host}/api/chat"
    payload={'model':model,'messages':msgs,'stream':stream}
    data=json.dumps(payload).encode('utf-8')
    req=urllib.request.Request(url,data=data,headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=120) as resp:
            if stream: return _stream_it(resp)
            else:
                r=json.loads(resp.read().decode('utf-8'))
                return r.get('message',{}).get('content','')
    except urllib.error.URLError as e: return f"[conn err: {e}]"
    except Exception as e: return f"[err: {e}]"

def _stream_it(resp):
    chunks=[]
    for ln in resp:
        if ln:
            c=json.loads(ln.decode('utf-8'))
            txt=c.get('message',{}).get('content','')
            if txt:
                chunks.append(txt)
                print(txt,end='',flush=True)
    print()
    return ''.join(chunks)

def generate(prompt,model=None,system=None):
    model=model or get_model()
    url=f"{ollama_host}/api/generate"
    payload={'model':model,'prompt':prompt,'stream':False}
    if system: payload['system']=system
    data=json.dumps(payload).encode('utf-8')
    req=urllib.request.Request(url,data=data,headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=120) as resp:
            r=json.loads(resp.read().decode('utf-8'))
            return r.get('response','')
    except Exception as e: return f"[err: {e}]"

def check_connection():
    url=f"{ollama_host}/api/tags"
    try:
        with urllib.request.urlopen(url,timeout=5) as resp:
            d=json.loads(resp.read().decode('utf-8'))
            models=[m['name'] for m in d.get('models',[])]
            return True,models
    except Exception as e: return False,str(e)
