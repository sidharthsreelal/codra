from brain.base import Agent

class Planner(Agent):
    name='planner'
    role='task planning'
    
    def system_prompt(s):
        return """Break down tasks into steps.

Plan: {"plan": [{"step": 1, "action": "desc", "agent": "coder/runner/reviewer"}]}
Or: {"delegate": "coder", "task": "desc"}

Agents: coder (code), runner (commands), reviewer (review)
JSON only."""

    def handle(s,task,ctx=None):
        resp=s.think(task,ctx)
        p=s.parse_response(resp)
        
        if 'plan' in p:
            steps=p['plan'];out=[]
            for st in steps:
                ag=st.get('agent','coder')
                act=st.get('action','')
                s.delegate(ag,act)
                out.append(f"-> {ag}: {act[:40]}")
            return {'status':'planned','steps':out}
        
        if 'delegate' in p:
            s.delegate(p['delegate'],p['task'])
            return {'status':'delegated','to':p['delegate']}
        
        return {'status':'response','content':p.get('answer',resp)}
