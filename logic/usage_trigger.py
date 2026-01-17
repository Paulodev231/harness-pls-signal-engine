import requests
import json

# MOCK CONFIGURATION
SALESFORCE_API_URL = "https://harness.my.salesforce.com/services/data/v53.0/sobjects/Lead/"
OUTREACH_API_URL = "https://api.outreach.io/api/v2/sequences/"
CLEARBIT_API_KEY = "sk_test_..."

def handler(event, context):
    """
    Triggered by a webhook when a user hits PQL threshold.
    """
    user_email = event['email']
    usage_metric = event['metric'] # e.g., 'ci_cd_deployments'
    count = event['count']

    print(f"Processing PQL: {user_email} | Trigger: {usage_metric} ({count})")

    # STEP 1: ENRICHMENT (Simulated)
    firmographics = enrich_lead(user_email)
    
    if firmographics['employees'] > 1000:
        segment = "Enterprise"
    else:
        segment = "Commercial"

    # STEP 2: MAP TO SALESFORCE LEAD
    sf_payload = {
        "FirstName": event['first_name'],
        "LastName": event['last_name'],
        "Company": firmographics['company_name'],
        "Email": user_email,
        "LeadSource": "Product Usage",
        "Status": "Open - High Intent",
        "Product_Interest__c": map_interest(usage_metric), # Custom Field
        "PQL_Score__c": calculate_score(count, segment)    # Custom Formula
    }

    # STEP 3: EXECUTE SYNC
    sf_response = requests.post(SALESFORCE_API_URL, json=sf_payload)
    
    if sf_response.status_code == 201:
        lead_id = sf_response.json()['id']
        print(f"Lead created in SFDC: {lead_id}")
        trigger_outreach_sequence(lead_id, segment, usage_metric)
    else:
        print(f"Error creating lead: {sf_response.text}")

def map_interest(metric):
    if "deploy" in metric: return "CI/CD"
    if "flag" in metric: return "Feature Flags"
    return "Platform"

def trigger_outreach_sequence(lead_id, segment, interest):
    # Logic to pick the right sequence ID based on segment + product interest
    # e.g., If Enterprise + CI/CD -> Sequence ID 1045
    pass
