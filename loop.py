from brain import Planner,Coder,Runner,Reviewer
from msg import Msg,Kind,get_bus
from mem import Session
import time

class Loop:
    def __init__(s,session=None):
        s.session=session or Session()
        s.bus=get_bus()
        s.agents={'planner':Planner(),'coder':Coder(),'runner':Runner(),'reviewer':Reviewer()}
        s.max_iter=20
        s.verbose=True
    
    def log(s,m):
        if s.verbose:print(f"[loop] {m}")
    
    def dispatch(s,task,entry='planner'):
        s.session.add_user(task)
        s.bus.send(Msg(kind=Kind.TASK,sender='user',content=task,target=entry))
        
        results=[];iters=0
        while iters<s.max_iter:
            did=False
            for name,agent in s.agents.items():
                if agent.has_work():
                    did=True
                    s.log(f"{name}...")
                    r=agent.run_once()
                    if r:
                        results.append({'agent':name,'result':r,'iter':iters})
                        s.log(f"{name} -> {r.get('status','?')}")
            if not did:break
            iters+=1
            time.sleep(0.1)
        
        final=s._sum(results)
        s.session.add_assistant(str(final))
        return final
    
    def _sum(s,results):
        if not results:return {'status':'no_action','results':[]}
        out={'status':'done','iters':len(set(r['iter'] for r in results)),'agents':list(set(r['agent'] for r in results)),'actions':[]}
        for r in results:
            res=r['result']
            st=res.get('status','')
            if st=='file_written':out['actions'].append(f"wrote {res.get('file')}")
            elif st=='success':out['actions'].append("cmd ok")
            elif st=='reviewed':out['actions'].append("reviewed")
            elif st=='delegated':out['actions'].append(f"-> {res.get('to')}")
        return out
    
    def quick(s,task):
        from tools.ask import query
        hist=s.session.get_chat_history()
        resp=query(task,history=hist)
        s.session.add_user(task)
        s.session.add_assistant(resp)
        return resp

def create_loop(session_name=None):
    sess=Session(session_name) if session_name else Session()
    return Loop(sess)
