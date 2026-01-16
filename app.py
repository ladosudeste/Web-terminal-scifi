from flask import Flask, render_template, request, jsonify
import subprocess
import os
import platform
import time

app = Flask(__name__)

def run(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return out.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exec", methods=["POST"])
def exec_cmd():
    cmd = request.json.get("cmd", "")

    if cmd in ["clear", "cls"]:
        return ""

    output = run(cmd)
    return output

@app.route("/status")
def status():
    data = {
        "kernel": {
            "os": platform.system(),
            "release": platform.release(),
            "arch": platform.machine(),
            "hostname": run("hostname"),
            "uptime": run("uptime -p"),
            "user": os.getenv("USER") or "unknown"
        },
        "cpu": {
            "model": run("cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2"),
            "cores": run("nproc"),
            "usage": run("top -bn1 | grep 'Cpu(s)'")
        },
        "memory": run("free -h"),
        "disk": run("df -h /"),
        "network": {
            "interfaces": run("ip addr | grep 'state UP'"),
            "ip": run("hostname -I"),
            "route": run("ip route | head -1"),
            "traffic": run("cat /proc/net/dev")
        }
    }
    return jsonify(data)

@app.route("/sysinfo")
def sysinfo():
    import os, platform, subprocess

    def cmd(c):
        try:
            return subprocess.check_output(
                c, shell=True, stderr=subprocess.DEVNULL, text=True
            ).strip()
        except:
            return ""

    def read(path):
        try:
            with open(path) as f:
                return f.read().strip()
        except:
            return ""

    # ===== AMBIENTE =====
    is_android = (
        os.path.exists("/system/build.prop")
        or "ANDROID_ROOT" in os.environ
        or "TERMUX_VERSION" in os.environ
    )

    # ===== UPTIME =====
    uptime_h = "N/A"
    up = read("/proc/uptime")
    if up:
        sec = float(up.split()[0])
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        uptime_h = f"{h}h {m}m"

    # ===== LOAD =====
    load = "N/A"
    la = read("/proc/loadavg")
    if la:
        load = " ".join(la.split()[:3])

    # ===== CPU =====
    cpuinfo = read("/proc/cpuinfo")
    cpu_model = "UNKNOWN"
    cores = "N/A"

    if cpuinfo:
        for key in ("model name", "Hardware", "Processor"):
            for line in cpuinfo.splitlines():
                if key in line:
                    cpu_model = line.split(":", 1)[1].strip()
                    break
            if cpu_model != "UNKNOWN":
                break
        cores = str(cpuinfo.count("processor"))

    # Android fallback (muito importante)
    if is_android and cpu_model == "UNKNOWN":
        cpu_model = (
            cmd("getprop ro.soc.model")
            or cmd("getprop ro.hardware")
            or cmd("getprop ro.board.platform")
            or "UNKNOWN"
        )

    # ===== MEM =====
    mem_total = mem_free = mem_avail = "N/A"
    meminfo = read("/proc/meminfo")
    if meminfo:
        for l in meminfo.splitlines():
            if l.startswith("MemTotal"):
                mem_total = l.split(":")[1].strip()
            elif l.startswith("MemFree"):
                mem_free = l.split(":")[1].strip()
            elif l.startswith("MemAvailable"):
                mem_avail = l.split(":")[1].strip()

    # ===== DISK =====
    disk = "N/A"
    if is_android:
        disk = cmd("df -h $HOME | tail -1") or cmd("df -h /data | tail -1")
    else:
        disk = cmd("df -h / | tail -1")

    # ===== IP =====
    ip = (
        cmd("hostname -I")
        or cmd("ip -o -4 addr show | awk '{print $4}'")
        or cmd("ifconfig | grep 'inet ' | grep -v 127 | awk '{print $2}'")
        or "N/A"
    )

    # ===== ROUTE =====
    route = (
        cmd("ip route | head -1")
        or cmd("route -n | awk 'NR==3{print}'")
        or "N/A"
    )

    # ===== ANDROID INFO =====
    android = ""
    if is_android:
        android = f"""
ANDROID ::
SDK     :: {cmd("getprop ro.build.version.sdk")}
RELEASE :: {cmd("getprop ro.build.version.release")}
MODEL   :: {cmd("getprop ro.product.model")}
BRAND   :: {cmd("getprop ro.product.brand")}
ABI     :: {cmd("getprop ro.product.cpu.abi")}
"""

    return f"""
SYSTEM ::
OS      :: {platform.system()}
KERNEL  :: {platform.release()}
ARCH    :: {platform.machine()}
HOST    :: {cmd("hostname") or "localhost"}
UPTIME  :: {uptime_h}
LOAD    :: {load}

CPU ::
MODEL   :: {cpu_model}
CORES   :: {cores}

MEMORY ::
TOTAL   :: {mem_total}
FREE    :: {mem_free}
AVAIL   :: {mem_avail}

DISK ::
{disk}

NETWORK ::
IP      :: {ip}
ROUTE   :: {route}
{android}
""".strip()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)