from flask import Flask, render_template_string, Response
import psutil
import time
import random

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Pipeline Frontend</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .metric { background: #e8f4fd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007acc; }
        .status-good { color: #28a745; font-weight: bold; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 DevOps Pipeline Frontend</h1>
        <div class="metric">
            <strong>Status:</strong> <span class="status-good">{{ status }}</span>
        </div>
        <div class="metric">
            <strong>CPU Usage:</strong> {{ cpu_percent }}%
        </div>
        <div class="metric">
            <strong>Memory Usage:</strong> {{ memory_percent }}%
        </div>
        <div class="metric">
            <strong>Uptime:</strong> {{ uptime }} seconds
        </div>
        <div class="metric">
            <strong>Total Requests:</strong> {{ request_count }}
        </div>
        <div class="metric">
            <strong>Last Updated:</strong> {{ timestamp }}
        </div>
        <div style="margin-top: 20px;">
            <a href="/health" style="background: #007acc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Health Check</a>
            <a href="/metrics" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">Metrics</a>
        </div>
    </div>
</body>
</html>
'''

start_time = time.time()
request_count = 0

def get_metrics():
    global request_count
    request_count += 1
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    uptime = int(time.time() - start_time)
    
    return {
        'cpu_percent': round(cpu_usage, 2),
        'memory_percent': round(memory.percent, 2),
        'uptime': uptime,
        'request_count': request_count,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def index():
    metrics = get_metrics()
    return render_template_string(HTML_TEMPLATE, 
        status='Running', 
        **metrics
    )

@app.route('/health')
def health():
    return {
        'status': 'healthy', 
        'service': 'frontend',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'uptime': int(time.time() - start_time)
    }

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    metrics = get_metrics()
    
    prometheus_metrics = f"""# HELP frontend_cpu_usage_percent CPU usage percentage
# TYPE frontend_cpu_usage_percent gauge
frontend_cpu_usage_percent {metrics['cpu_percent']}

# HELP frontend_memory_usage_percent Memory usage percentage  
# TYPE frontend_memory_usage_percent gauge
frontend_memory_usage_percent {metrics['memory_percent']}

# HELP frontend_uptime_seconds Service uptime in seconds
# TYPE frontend_uptime_seconds counter
frontend_uptime_seconds {metrics['uptime']}

# HELP frontend_requests_total Total number of requests
# TYPE frontend_requests_total counter
frontend_requests_total {metrics['request_count']}

# HELP frontend_up Service availability
# TYPE frontend_up gauge
frontend_up 1
"""
    
    return Response(prometheus_metrics, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)