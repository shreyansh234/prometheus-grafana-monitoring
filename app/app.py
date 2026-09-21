from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import random
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests received by the application"
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Application request latency in seconds"
)

@app.route("/")
def home():
    REQUEST_COUNT.inc()

    start_time = time.time()
    time.sleep(random.uniform(0.05, 0.3))
    REQUEST_LATENCY.observe(time.time() - start_time)

    return """
    <h1>DevOps Monitoring Application</h1>
    <h2>Prometheus + Grafana</h2>
    <p>Application is running successfully.</p>
    <p>Metrics are available at <b>/metrics</b></p>
    """

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)