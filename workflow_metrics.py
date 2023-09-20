import requests
import json

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

    # Expose metrics in Prometheus format
    prometheus_metrics = f"""\
# HELP workflow_success_rate Success rate of workflows
# TYPE workflow_success_rate gauge
workflow_success_rate {{"repository"="{owner}/{repo}"}} {success_workflows / total_workflows}

# HELP workflow_failure_rate Failure rate of workflows
# TYPE workflow_failure_rate gauge
workflow_failure_rate {{"repository"="{owner}/{repo}"}} {failure_workflows / total_workflows}
"""

    print(prometheus_metrics)
else:
    print(f"Failed to fetch workflow runs: {response.status_code}")
