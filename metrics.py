from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, start_http_server
import os
import requests
import time

# Function to fetch workflow runs from GitHub API
def fetch_workflow_runs(repository, token):
    url = f"https://api.github.com/repos/{repository}/actions/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to calculate success rate and failure rate
def calculate_success_failure_rate(runs):
    total_runs = len(runs)
    success_count = sum(1 for run in runs if run["conclusion"] == "success")
    failure_count = sum(1 for run in runs if run["conclusion"] == "failure")
    success_rate = success_count / total_runs if total_runs > 0 else 0
    failure_rate = failure_count / total_runs if total_runs > 0 else 0
    return success_rate, failure_rate
  
# Create a registry to hold the metric
registry = CollectorRegistry()

# Create a Gauge metric for success rate and failure rate
success_rate_metric = Gauge("github_actions_success_rate", "GitHub Actions Success Rate", ["repository"])
failure_rate_metric = Gauge("github_actions_failure_rate", "GitHub Actions Failure Rate", ["repository"])

# Replace with your GitHub repository and token
repository_name = os.getenv("GITHUB_REPOSITORY")
github_token = os.getenv("GITHUB_TOKEN")

# Fetch workflow runs from GitHub API
workflow_runs = fetch_workflow_runs(repository_name, github_token)

# Calculate success rate and failure rate
success_rate, failure_rate = calculate_success_failure_rate(workflow_runs["workflow_runs"])

# Set the success rate and failure rate in metrics
success_rate_metric.labels(repository=repository_name).set(success_rate)
failure_rate_metric.labels(repository=repository_name).set(failure_rate)

# Start an HTTP server on port 8000 for Prometheus to scrape
start_http_server(8000)

# Push the metrics to the Prometheus server (replace the URL with your Prometheus server URL)
prometheus_server_url = "prometheus.example.com:9091"
push_to_gateway(prometheus_server_url, job="github_actions_metrics", registry=registry)

# Sleep for a while to allow Prometheus to scrape the metrics
time.sleep(30)
