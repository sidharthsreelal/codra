from llm import chat,generate

def query(prompt,history=None,system=None):
    msgs=[]
    if system: msgs.append({'role':'system','content':system})
    if history: msgs.extend(history)
    msgs.append({'role':'user','content':prompt})
    return chat(msgs)

def quick(prompt,system=None):
    return generate(prompt,system=system)

def decide(q,opts,ctx=None):
    p=f"Options: {opts}\n\nQuestion: {q}"
    if ctx: p=f"Context: {ctx}\n\n{p}"
    p+="\n\nRespond with ONLY the chosen option."
    return quick(p).strip()

def extract_code(txt):
    lines=txt.split('\n')
    inside=False
    out=[]
    for ln in lines:
        if ln.strip().startswith('```'):
            if inside: break
            inside=True
            continue
        if inside: out.append(ln)
    if out: return '\n'.join(out)
    return txt

def summarize(txt,maxlen=200):
    return quick(f"Summarize in under {maxlen} chars:\n\n{txt}")
