from dataclasses import dataclass,field
from typing import Any,Optional
from enum import Enum
import uuid,time

class Kind(Enum):
    TASK='task'
    RESULT='result'
    DELEGATE='delegate'
    QUERY='query'
    ERROR='error'

@dataclass
class Msg:
    kind:Kind
    sender:str
    content:Any
    target:Optional[str]=None
    id:str=field(default_factory=lambda:str(uuid.uuid4())[:8])
    ts:float=field(default_factory=time.time)
    meta:dict=field(default_factory=dict)

class Bus:
    def __init__(self):
        self._q={}
        self._hist=[]
    
    def register(self,name):
        if name not in self._q:self._q[name]=[]
    
    def send(self,msg):
        self._hist.append(msg)
        if msg.target and msg.target in self._q:
            self._q[msg.target].append(msg)
        elif msg.target is None:
            for q in self._q.values():q.append(msg)
    
    def receive(self,name):
        if name in self._q and self._q[name]:return self._q[name].pop(0)
        return None
    
    def peek(self,name):
        if name in self._q and self._q[name]:return self._q[name][0]
        return None
    
    def has_pending(self,n):return n in self._q and len(self._q[n])>0
    def get_history(self,lim=50):return self._hist[-lim:]
    
    def clear(self,name=None):
        if name:self._q[name]=[]
        else:
            for k in self._q:self._q[k]=[]

_bus=Bus()
def get_bus():return _bus
