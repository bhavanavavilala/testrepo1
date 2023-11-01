name: component-version 

on: workflow_dispatch

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - uses: jannekem/run-python-script-action@v1
        with:
          script: |
            import yaml
 
            # Define the chart.yaml content as a multi-line string
            chart_yaml_content = """
            apiVersion: v2
            name: my-chart
            description: A Helm chart example with dependencies
            version: 0.1.0
 
            dependencies:
              - name: nginx
                version: 1.2.3
                repository: https://example.com/charts
              - name: redis
                version: 2.0.1
                repository: https://example.com/charts
              - name: mariadb
                version: 3.5.0
                repository: https://example.com/charts
            """
 
            # Load the chart.yaml content as YAML
            chart_data = yaml.safe_load(chart_yaml_content)
 
            # Extract component and version information
            components = chart_data.get("dependencies", [])
            component_info = [(component["name"], component["version"]) for component in components]
 
            # Display the information in a table
            print("Component Name\t\tVersion")
            print("---------------\t\t-------")
            for name, version in component_info:
                print(f"{name}\t\t\t{version}")
