#!/usr/bin/env python3
"""Process monitor — track CPU/memory of running processes."""
import sys, subprocess, time, json

def get_procs(sort_by='cpu', limit=10):
    cmd = ['ps', 'aux', '--sort', f'-{sort_by}' if sys.platform != 'darwin' else f'-o pid,pcpu,pmem,rss,comm']
    if sys.platform == 'darwin':
        cmd = ['ps', 'axo', 'pid,pcpu,pmem,rss,comm']
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    header = lines[0]; procs = []
    for line in lines[1:limit+1]:
        parts = line.split(None, 4)
        if len(parts) >= 5:
            procs.append({'pid':parts[0],'cpu':parts[1],'mem':parts[2],'rss':parts[3],'command':parts[4][:50]})
    return procs

def watch(pattern=None, interval=2, count=5):
    for i in range(count):
        procs = get_procs(limit=20)
        if pattern:
            procs = [p for p in procs if pattern.lower() in p['command'].lower()]
        print(f"\n{'PID':>7} {'CPU%':>6} {'MEM%':>6} {'RSS MB':>8}  Command")
        print('-' * 60)
        for p in procs[:10]:
            rss_mb = int(p['rss'])/1024
            print(f"{p['pid']:>7} {p['cpu']:>6} {p['mem']:>6} {rss_mb:>8.1f}  {p['command']}")
        if i < count-1: time.sleep(interval)

if __name__ == '__main__':
    if '--watch' in sys.argv:
        pattern = sys.argv[2] if len(sys.argv) > 2 else None
        watch(pattern)
    elif '--json' in sys.argv:
        print(json.dumps(get_procs(), indent=2))
    elif len(sys.argv) > 1:
        watch(sys.argv[1], count=1)
    else:
        watch(count=1)
