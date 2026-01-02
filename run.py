import argparse,sys
from llm import check_connection
from cfg import get_model,set_model
from loop import create_loop
from mem import list_sessions,new_session

def banner():
    print("codra - local ai coding")
    print("'help' for cmds, 'quit' to exit\n")

def helpme():
    print("""
cmds:
  help       - this
  quit/exit  - bye
  model      - show model
  model X    - set model
  sessions   - list sessions
  new        - new session
  clear      - clear screen
  quick      - direct llm

anything else -> agents
""")

def chk_ollama():
    ok,info=check_connection()
    if not ok:
        print(f"[!] ollama down: {info}")
        print("    run: ollama serve")
        return False
    print("[ok] ollama connected")
    if info:print(f"     models: {', '.join(info[:5])}")
    return True

def repl(loop):
    while True:
        try:inp=input("\n> ").strip()
        except:print("\nbye");break
        
        if not inp:continue
        cmd=inp.lower()
        
        if cmd in ('quit','exit','q'):print("bye");break
        if cmd=='help':helpme();continue
        if cmd=='model':print(f"model: {get_model()}");continue
        if cmd.startswith('model '):
            n=inp[6:].strip()
            set_model(n)
            print(f"model -> {n}")
            continue
        if cmd=='sessions':
            ss=list_sessions()
            for s in ss[:10]:print(f"  - {s}")
            if not ss:print("none")
            continue
        if cmd=='new':
            loop=create_loop()
            print("new session")
            continue
        if cmd=='clear':print("\033[2J\033[H",end='');continue
        if cmd=='quick':
            print("quick mode (direct llm)")
            try:
                q=input("? ").strip()
                if q:print(loop.quick(q))
            except:pass
            continue
        
        print("[thinking...]")
        try:
            r=loop.dispatch(inp)
            print()
            for a in r.get('actions',[]):print(f"  - {a}")
            print(f"\n[done] {r.get('status','ok')}")
        except Exception as e:print(f"[err] {e}")

def main():
    parser=argparse.ArgumentParser(description='codra')
    parser.add_argument('--test-llm',action='store_true')
    parser.add_argument('--model',type=str)
    parser.add_argument('--session',type=str)
    parser.add_argument('task',nargs='*')
    args=parser.parse_args()
    
    if args.model:set_model(args.model)
    if args.test_llm:
        if chk_ollama():print("ok");sys.exit(0)
        sys.exit(1)
    if not chk_ollama():sys.exit(1)
    
    loop=create_loop(args.session)
    if args.task:
        print(loop.dispatch(' '.join(args.task)))
        return
    
    banner()
    repl(loop)

if __name__=='__main__':main()
