from brain.base import Agent

class Runner(Agent):
    name='runner'
    role='command execution'
    
    def system_prompt(s):
        return """Run shell commands.

Run: {"tool": "run_cmd", "args": {"cmd": "echo hi"}}
List: {"tool": "list_dir", "args": {"path": "."}}
Success: {"answer": "worked: ..."}
Fail: {"delegate": "coder", "task": "fix: ..."}

JSON only."""

    def handle(s,task,ctx=None):
        retries=3;last=None
        for _ in range(retries):
            c=ctx or ''
            if last:c+=f"\n\nOutput:\n{last}"
            resp=s.think(task,c)
            p=s.parse_response(resp)
            
            if 'tool' in p:
                r,e=s.execute_tool(p['tool'],p.get('args',{}))
                if p['tool']=='run_cmd' and r:
                    last=f"out: {r.get('stdout','')}\nerr: {r.get('stderr','')}"
                    if r.get('ok'):
                        return {'status':'success','output':r.get('stdout',''),'code':r.get('code',0)}
                    if 'delegate' in p:s.delegate(p['delegate'],p.get('task',f'fix: {last}'))
                    continue
                return {'status':'tool_result','result':r,'error':e}
            
            if 'delegate' in p:
                s.delegate(p['delegate'],p['task'])
                return {'status':'delegated','to':p['delegate']}
            
            return {'status':'response','content':p.get('answer',resp)}
        return {'status':'failed','last_output':last}
