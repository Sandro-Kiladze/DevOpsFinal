from flask import Flask, jsonify, Response
import time
import psutil
import random

app = Flask(__name__)
start_time = time.time()
request_count = 0
api_calls = 0

def get_system_metrics():
    global request_count, api_calls
    request_count += 1
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime = int(time.time() - start_time)
    
    return {
        'cpu_percent': round(cpu_usage, 2),
        'memory_percent': round(memory.percent, 2),
        'disk_percent': round(disk.percent, 2),
        'uptime': uptime,
        'request_count': request_count,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/api/status')
def status():
    global api_calls
    api_calls += 1
    metrics = get_system_metrics()
    
    return jsonify({
        'service': 'backend',
        'status': 'running',
        'api_calls': api_calls,
        **metrics
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'backend',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'uptime': int(time.time() - start_time)
    })

@app.route('/api/metrics')
def api_metrics():
    metrics = get_system_metrics()
    return jsonify(metrics)

@app.route('/metrics')
def prometheus_metrics():
    """Prometheus metrics endpoint"""
    global api_calls
    metrics = get_system_metrics()
    
    prometheus_data = f"""# HELP backend_cpu_usage_percent CPU usage percentage
# TYPE backend_cpu_usage_percent gauge
backend_cpu_usage_percent {metrics['cpu_percent']}

# HELP backend_memory_usage_percent Memory usage percentage
# TYPE backend_memory_usage_percent gauge
backend_memory_usage_percent {metrics['memory_percent']}

# HELP backend_disk_usage_percent Disk usage percentage
# TYPE backend_disk_usage_percent gauge
backend_disk_usage_percent {metrics['disk_percent']}

# HELP backend_uptime_seconds Service uptime in seconds
# TYPE backend_uptime_seconds counter
backend_uptime_seconds {metrics['uptime']}

# HELP backend_requests_total Total number of requests
# TYPE backend_requests_total counter
backend_requests_total {metrics['request_count']}

# HELP backend_api_calls_total Total API calls
# TYPE backend_api_calls_total counter
backend_api_calls_total {api_calls}

# HELP backend_up Service availability
# TYPE backend_up gauge
backend_up 1
"""
    
    return Response(prometheus_data, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)