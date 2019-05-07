"""
Copyright (c) 2018 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
                https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import json
import requests

from chalice import Chalice

app = Chalice(app_name='SWC-Webhook')

# ServiceNow Variables
SNOW_USERNAME = ""
SNOW_PASSWORD = ""
SNOW_TENANT = ""


@app.route('/', methods=['POST'])
def event():
    """A function to process the inbound webhook"""

    # Get the current request
    request = app.current_request

    # Get the event data from the request
    json_data = request.json_body

    # Send the event data to ServiceNow
    response = _post_to_servicenow(json_data)

    # Return the ServiceNow response
    return response


def _post_to_servicenow(event_data):
    """A function to POST event data to ServiceNow to create an incident"""

    # Build the ServiceNow API URL
    SNOW_URL = 'https://{}.service-now.com/api/now/table/incident'.format(SNOW_TENANT)

    # Specify headers for the ServiceNow POST request
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    data = {
        "category": "Network",
        "impact": 2,
        "urgency": 2,
        "short_description": "Stealtwatch Cloud Alert: {}".format(event_data['description']),
        "description": json.dumps(event_data, indent=4)
    }

    # Send the data to ServiceNow
    response = requests.post(SNOW_URL, auth=(SNOW_USERNAME, SNOW_PASSWORD), headers=headers, data=json.dumps(data))

    # Print logging
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())

    return response.json()
