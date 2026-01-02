from brain.base import Agent
from tools.ask import extract_code

class Coder(Agent):
    name='coder'
    role='code writing'
    
    def system_prompt(s):
        return """Write/edit code files.

Write: {"tool": "write_file", "args": {"path": "f.py", "content": "code"}}
Read: {"tool": "read_file", "args": {"path": "f.py"}}
Dir: {"tool": "make_dir", "args": {"path": "dir"}}
Code: {"code": "...", "file": "path.py"}

No comments. No docstrings. JSON only."""

    def handle(s,task,ctx=None):
        tries=3;last=None
        for _ in range(tries):
            c=ctx or ''
            if last:c+=f"\n\nPrev: {last}"
            resp=s.think(task,c)
            p=s.parse_response(resp)
            
            if 'tool' in p:
                r,e=s.execute_tool(p['tool'],p.get('args',{}))
                if e:last=f"err: {e}";continue
                return {'status':'tool_executed','tool':p['tool'],'result':r}
            
            if 'code' in p:
                fp=p.get('file','out.py')
                r,e=s.execute_tool('write_file',{'path':fp,'content':p['code']})
                if e:last=f"write err: {e}";continue
                return {'status':'file_written','file':fp}
            
            code=extract_code(resp)
            if code and code!=resp:return {'status':'code_generated','code':code}
            return {'status':'response','content':p.get('answer',resp)}
        return {'status':'failed','error':last}
