import requests

from requests.auth import HTTPBasicAuth


headers = {'Content-Type': 'application/json'}
# Making a get request
#data = b'{\n  "incident": {\n    "condition": {\n      "conditionThreshold": {\n        "aggregations": [\n          {\n            "alignmentPeriod": "120s",\n            "perSeriesAligner": "ALIGN_MEAN"\n          }\n        ],\n        "comparison": "COMPARISON_GT",\n        "duration": "300s",\n        "filter": "resource.type = \\"cloudsql_database\\" AND metric.type = \\"cloudsql.googleapis.com/database/cpu/utilization\\" AND metadata.system_labels.name = \\"wkingdb\\"",\n        "thresholdValue": 0.05,\n        "trigger": {\n          "count": 1\n        }\n      },\n      "displayName": "Cloud SQL Database - CPU utilization",\n      "name": "projects/owin-337303/alertPolicies/5056611904621304961/conditions/1425791100892547978"\n    },\n    "condition_name": "Cloud SQL Database - CPU utilization",\n    "ended_at": null,\n    "incident_id": "0.mwq7zl92ky7a",\n    "metadata": {\n      "system_labels": {\n        "name": "wkingdb"\n      },\n      "user_labels": {}\n    },\n    "metric": {\n      "displayName": "CPU utilization",\n      "labels": {},\n      "type": "cloudsql.googleapis.com/database/cpu/utilization"\n    },\n    "observed_value": "0.109",\n    "policy_name": "alert-wkingdb-cpu-utilization",\n    "resource": {\n      "labels": {\n        "database_id": "owin-337303:wkingdb",\n        "project_id": "owin-337303",\n        "region": "asia-southeast1"\n      },\n      "type": "cloudsql_database"\n    },\n    "resource_display_name": "wkingdb_localtest",\n    "resource_id": "",\n    "resource_name": "owin-337303 wkingdb",\n    "resource_type_display_name": "Cloud SQL Database",\n    "scoping_project_id": "owin-337303",\n    "scoping_project_number": 31816715395,\n    "started_at": 1682588023,\n    "state": "open",\n    "summary": "CPU utilization for owin-337303 wkingdb with system labels {name=wkingdb} is above the threshold of 0.050 with a value of 0.109.",\n    "threshold_value": "0.05",\n    "url": "https://console.cloud.google.com/monitoring/alerting/incidents/0.mwq7zl92ky7a?project=owin-337303"\n  },\n  "version": "1.2"\n}'
response = requests.post('https://cloudsql-webhook.owin.info/basic-auth',
            headers=headers,
            #data=data,
            auth = HTTPBasicAuth('admin', 'secret'))
  
# print request object
print(response.status_code)