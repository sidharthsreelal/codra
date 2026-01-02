import json,time
from pathlib import Path
from cfg import session_dir

class Sess:
    def __init__(s,name=None):
        s.name=name or f"s_{int(time.time())}"
        s.path=session_dir/f"{s.name}.json"
        s.messages=[];s.context={};s.created=time.time()
        s._load()
    
    def _load(s):
        if s.path.exists():
            with open(s.path) as f:
                d=json.load(f)
                s.messages=d.get('messages',[])
                s.context=d.get('context',{})
                s.created=d.get('created',s.created)
    
    def save(s):
        d={'name':s.name,'messages':s.messages,'context':s.context,'created':s.created,'updated':time.time()}
        with open(s.path,'w') as f:json.dump(d,f,indent=2)
    
    def add_user(s,c):s.messages.append({'role':'user','content':c,'ts':time.time()});s.save()
    def add_assistant(s,c):s.messages.append({'role':'assistant','content':c,'ts':time.time()});s.save()
    def add_system(s,c):s.messages.append({'role':'system','content':c,'ts':time.time()});s.save()
    
    def get_chat_history(s,lim=20):
        recent=s.messages[-lim:] if len(s.messages)>lim else s.messages
        return [{'role':m['role'],'content':m['content']} for m in recent]
    
    def set_ctx(s,k,v):s.context[k]=v;s.save()
    def get_ctx(s,k,d=None):return s.context.get(k,d)

Session=Sess
def list_sessions():return [p.stem for p in session_dir.glob('*.json')]
def load_session(n):return Sess(n)
def new_session():return Sess()
