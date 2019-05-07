# Stealthwatch Cloud (SWC) Webhook to ServiceNow

This script is meant as proof-of-concept code for taking in Stealthwatch Cloud webhook events to create ServiceNow incidents.

## Configuration

### ServiceNow
***
In the [app.py](SWC-Webhook/app.py) file you'll need to provide three configuration items for ServiceNow:

* Username (SNOW_USERNAME)
* Password (SNOW_PASSWORD)
* Tenant (SNOW_TENANT)

### AWS Lambda
***
This script was built using the [AWS Chalice](https://github.com/aws/chalice) micro-framework.

The easiest way to get this off the ground is by doing the following from the base project directory:

```bash
python3 -m venv venv
source venv/bin/activate
cd SWC-Webhook
pip install -r requirements.txt
chalice deploy
```

This will deploy the AWS Lambda function, and give you a Rest API URL like the following:

```
https://abc123.execute-api.us-east-1.amazonaws.com/api/
```

Stealthwatch Cloud will need to be provided with that URL.

### Stealthwatch Cloud
***
In Stealthwatch Cloud, follow the steps below to finish configuration.

1. In the SWC web interface, click on the gear/cog icon in the upper right-hand corner, then select **Services/Webhooks**
2. In the left-hand menu, select **Webhooks**
3. In the **HTTP/HTTPS URL** field, enter your Lambda function's Rest API URL.
4. Make sure **Output Format** field is set to JSON.
5. Click Add

This should send a test event to your Lambda function, and create an event in ServiceNow.

> **NOTE:** If the webhook fails, you can click on the "Recent Deliveries" entry in the Stealthwatch Cloud UI to see the request and response, and even re-send the webhook.  **It often takes a few minutes for the Lambda function to fully initialize.**

Future events will perform the same task, but will populate the ServiceNow incident with real event data.
