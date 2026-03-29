#!/usr/bin/env python3
"""proc_monitor - Process monitoring with CPU/memory tracking simulation."""
import sys, time, random

class ProcessInfo:
    def __init__(self, pid, name, cpu=0, memory=0, status="running"):
        self.pid = pid; self.name = name; self.cpu = cpu
        self.memory = memory; self.status = status; self.start_time = time.time()
    def uptime(self):
        return time.time() - self.start_time

class ProcessMonitor:
    def __init__(self):
        self.processes = {}
        self.history = {}
        self.alerts = []
    def add(self, proc):
        self.processes[proc.pid] = proc
        self.history[proc.pid] = []
    def sample(self):
        for pid, proc in self.processes.items():
            self.history[pid].append({"cpu": proc.cpu, "memory": proc.memory, "time": time.time()})
    def update(self, pid, cpu=None, memory=None, status=None):
        if pid in self.processes:
            p = self.processes[pid]
            if cpu is not None: p.cpu = cpu
            if memory is not None: p.memory = memory
            if status is not None: p.status = status
    def check_alerts(self, cpu_threshold=90, mem_threshold=90):
        alerts = []
        for pid, proc in self.processes.items():
            if proc.cpu > cpu_threshold:
                alerts.append({"pid": pid, "name": proc.name, "type": "cpu", "value": proc.cpu})
            if proc.memory > mem_threshold:
                alerts.append({"pid": pid, "name": proc.name, "type": "memory", "value": proc.memory})
        self.alerts.extend(alerts)
        return alerts
    def top(self, n=5, sort_by="cpu"):
        procs = list(self.processes.values())
        procs.sort(key=lambda p: getattr(p, sort_by, 0), reverse=True)
        return procs[:n]
    def avg_cpu(self, pid):
        h = self.history.get(pid, [])
        if not h: return 0
        return sum(s["cpu"] for s in h) / len(h)

def test():
    mon = ProcessMonitor()
    mon.add(ProcessInfo(1, "nginx", cpu=15, memory=30))
    mon.add(ProcessInfo(2, "python", cpu=95, memory=60))
    mon.add(ProcessInfo(3, "postgres", cpu=40, memory=95))
    mon.sample()
    alerts = mon.check_alerts()
    assert len(alerts) == 2
    assert any(a["name"] == "python" and a["type"] == "cpu" for a in alerts)
    assert any(a["name"] == "postgres" and a["type"] == "memory" for a in alerts)
    top = mon.top(2, "cpu")
    assert top[0].name == "python"
    assert len(top) == 2
    mon.update(2, cpu=10)
    assert mon.processes[2].cpu == 10
    assert mon.avg_cpu(1) == 15
    print("OK: proc_monitor")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: proc_monitor.py test")
