from flask import Flask, jsonify, render_template_string
import psutil
import subprocess

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>System Monitor</title>
    <style>
        body {
            font-family: monospace;
            background: #0f0f0f;
            color: #00ff00;
            padding: 40px;
        }
        h1 { color: #00ff00; }
        .card {
            background: #1a1a1a;
            border: 1px solid #00ff00;
            padding: 20px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .bar-bg {
            background: #333;
            height: 20px;
            border-radius: 4px;
            margin-top: 8px;
        }
        .bar-fill {
            background: #00ff00;
            height: 20px;
            border-radius: 4px;
            transition: width 0.5s;
        }
        .stat { font-size: 1.4em; margin: 4px 0; }
    </style>
</head>
<body>
    <h1>🖥️ System Monitor</h1>
    <p>Updates every 3 seconds</p>

    <div class="card">
        <h2>CPU</h2>
        <div class="stat" id="cpu">Loading...</div>
        <div class="bar-bg"><div class="bar-fill" id="cpu-bar" style="width:0%"></div></div>
    </div>

    <div class="card">
        <h2>RAM</h2>
        <div class="stat" id="ram">Loading...</div>
        <div class="bar-bg"><div class="bar-fill" id="ram-bar" style="width:0%"></div></div>
    </div>

    <div class="card">
        <h2>Disk</h2>
        <div class="stat" id="disk">Loading...</div>
        <div class="bar-bg"><div class="bar-fill" id="disk-bar" style="width:0%"></div></div>
    </div>

    <div class="card">
        <h2>Running Containers</h2>
        <div id="containers">Loading...</div>
    </div>

    <script>
        async function update() {
            const res = await fetch('/api/stats');
            const data = await res.json();

            document.getElementById('cpu').textContent =
                `${data.cpu.percent}% — ${data.cpu.cores} cores`;
            document.getElementById('cpu-bar').style.width =
                `${data.cpu.percent}%`;

            document.getElementById('ram').textContent =
                `${data.ram.used_gb} GB / ${data.ram.total_gb} GB (${data.ram.percent}%)`;
            document.getElementById('ram-bar').style.width =
                `${data.ram.percent}%`;

            document.getElementById('disk').textContent =
                `${data.disk.used_gb} GB / ${data.disk.total_gb} GB (${data.disk.percent}%)`;
            document.getElementById('disk-bar').style.width =
                `${data.disk.percent}%`;

            const containers = data.containers;
            if (containers.length === 0) {
                document.getElementById('containers').textContent =
                    'No containers running';
            } else {
                document.getElementById('containers').innerHTML =
                    containers.map(c => `<div>▸ ${c}</div>`).join('');
            }
        }

        update();
        setInterval(update, 3000);
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/stats")
def stats():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count()

    # RAM
    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024**3), 1)
    ram_used = round(ram.used / (1024**3), 1)

    # Disk
    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024**3), 1)
    disk_used = round(disk.used / (1024**3), 1)

    # Running containers
    containers = ["container visibility requires host mode"]

    return jsonify({
        "cpu": {
            "percent": cpu_percent,
            "cores": cpu_cores
        },
        "ram": {
            "total_gb": ram_total,
            "used_gb": ram_used,
            "percent": ram.percent
        },
        "disk": {
            "total_gb": disk_total,
            "used_gb": disk_used,
            "percent": disk.percent
        },
        "containers": containers
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
