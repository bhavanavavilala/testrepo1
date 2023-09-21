import requests
import json
from prometheus_client import start_http_server, Gauge

# Replace with your GitHub Personal Access Token
token = "GB_TOKEN"

# Replace with your GitHub repository owner and name
owner = "bhavanavavilala"
repo = "testrepo1"

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

# Get workflow runs
response = requests.get(
    f"https://api.github.com/repos/{owner}/{repo}/actions/runs",
    headers=headers,
)

if response.status_code == 200:
    data = response.json()
    total_workflows = len(data["workflow_runs"])
    success_workflows = sum(1 for run in data["workflow_runs"] if run["conclusion"] == "success")
    failure_workflows = sum(1 for run in data["workflow_runs"] if run["conclusion"] == "failure")

    # Create Prometheus metrics
    workflow_success_rate = Gauge('workflow_success_rate', 'Success rate of workflows')
    workflow_failure_rate = Gauge('workflow_failure_rate', 'Failure rate of workflows')

    # Calculate success and failure rates
    success_rate = success_workflows / total_workflows
    failure_rate = failure_workflows / total_workflows

    # Set the metrics values
    workflow_success_rate.set(success_rate)
    workflow_failure_rate.set(failure_rate)

    # Start the HTTP server to expose metrics
    start_http_server(8000)

    # Expose metrics in Prometheus format
    prometheus_metrics = f"""\
    # Metrics are already being exposed by Prometheus server
    """

    print(prometheus_metrics)
else:
    print(f"Failed to fetch workflow runs: {response.status_code}")
