import requests, os
from dotenv import load_dotenv

def request_token():
    load_dotenv('./lucas_env.env')
    apikey = os.getenv("CIS_SERVICES_APIKEY")
    data={'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': apikey}
    headers= {'Accept': 'application/json',
            'Content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic Yng6Yng='}
    url="https://iam.cloud.ibm.com/identity/token"
    token = requests.post(url=url, data=data, headers=headers)
    return token.json()["refresh_token"]