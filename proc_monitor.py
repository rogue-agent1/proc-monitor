#!/usr/bin/env python3
"""Process monitor — track CPU/memory of running processes."""
import subprocess,re,sys,time,json
def get_processes(sort_by="cpu",limit=10):
    cmd=["/bin/ps","aux"]; result=subprocess.run(cmd,capture_output=True,text=True)
    lines=result.stdout.strip().split("\n"); procs=[]
    for line in lines[1:]:
        parts=line.split(None,10)
        if len(parts)<11: continue
        procs.append({"user":parts[0],"pid":int(parts[1]),"cpu":float(parts[2]),"mem":float(parts[3]),"vsz":int(parts[4]),"rss":int(parts[5]),"command":parts[10]})
    key={"cpu":"cpu","mem":"mem","rss":"rss"}.get(sort_by,"cpu")
    return sorted(procs,key=lambda p:p[key],reverse=True)[:limit]
def summary():
    procs=get_processes(limit=1000)
    return {"total":len(procs),"total_cpu":sum(p["cpu"] for p in procs),"total_mem":sum(p["mem"] for p in procs),"top_cpu":procs[0] if procs else None}
if __name__=="__main__":
    top=get_processes(limit=5)
    for p in top: print(f"PID {p['pid']:6d} CPU={p['cpu']:5.1f}% MEM={p['mem']:5.1f}% {p['command'][:60]}")
    s=summary(); print(f"\nTotal: {s['total']} processes, {s['total_cpu']:.1f}% CPU, {s['total_mem']:.1f}% MEM")
    print("Process monitor OK")
