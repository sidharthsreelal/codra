from brain.base import Agent

class Reviewer(Agent):
    name='reviewer'
    role='code review'
    
    def system_prompt(s):
        return """Review code quality.

Read: {"tool": "read_file", "args": {"path": "f.py"}}
Review: {"review": {"quality": "good/ok/poor", "issues": [], "approved": true}}
Fix: {"delegate": "coder", "task": "fix: ..."}

JSON only."""

    def handle(s,task,ctx=None):
        c=ctx or ''
        if '.py' in task or '.js' in task:
            for p in task.split():
                if '.' in p and not p.startswith('.'):
                    content,e=s.execute_tool('read_file',{'path':p})
                    if not e and content:c+=f"\n\n{p}:\n{content}"
                    break
        
        resp=s.think(task,c)
        p=s.parse_response(resp)
        
        if 'review' in p:
            rev=p['review']
            if not rev.get('approved',True):
                issues=rev.get('issues',[])
                if issues:s.delegate('coder',f"fix: {', '.join(issues)}")
            return {'status':'reviewed','review':rev}
        
        if 'delegate' in p:
            s.delegate(p['delegate'],p['task'])
            return {'status':'delegated','to':p['delegate']}
        
        return {'status':'response','content':p.get('answer',resp)}
