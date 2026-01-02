from abc import ABC,abstractmethod
from msg import Msg,Kind,get_bus
from tools import fs,sh
from tools.ask import query,extract_code
import json

class Agent(ABC):
    name='base'
    role='generic'
    
    def __init__(s):
        s.bus=get_bus()
        s.bus.register(s.name)
        s._tools=s._init_tools()
    
    def _init_tools(s):
        return {'read_file':fs.read_file,'write_file':fs.write_file,'list_dir':fs.list_dir,'run_cmd':sh.run,'make_dir':fs.make_dir}
    
    def system_prompt(s):
        tls=', '.join(s._tools.keys())
        return f"""You are {s.name}, a {s.role}.
Tools: {tls}

Use tool: {{"tool": "name", "args": {{"k": "v"}}}}
Delegate: {{"delegate": "agent", "task": "desc"}}
Answer: {{"answer": "response"}}

JSON only."""

    def think(s,task,ctx=None):
        hist=[]
        if ctx:hist.append({'role':'system','content':ctx})
        return query(f"Task: {task}",history=hist,system=s.system_prompt())
    
    def parse_response(s,resp):
        try:
            c=resp.strip()
            if c.startswith('```'):c=extract_code(c)
            return json.loads(c)
        except:return {'answer':resp}
    
    def execute_tool(s,name,args):
        if name not in s._tools:return None,f"unknown: {name}"
        try:
            fn=s._tools[name]
            r=fn(**args) if isinstance(args,dict) else fn(args)
            return r,None
        except Exception as e:return None,str(e)
    
    def delegate(s,target,task):
        s.bus.send(Msg(kind=Kind.DELEGATE,sender=s.name,content=task,target=target))
    
    def send_result(s,content,target=None):
        s.bus.send(Msg(kind=Kind.RESULT,sender=s.name,content=content,target=target))
    
    def receive(s):return s.bus.receive(s.name)
    def has_work(s):return s.bus.has_pending(s.name)
    
    @abstractmethod
    def handle(s,task,ctx=None):pass
    
    def run_once(s):
        msg=s.receive()
        if msg:
            r=s.handle(msg.content,ctx=msg.meta.get('context'))
            if msg.sender!=s.name:s.send_result(r,target=msg.sender)
            return r
        return None
