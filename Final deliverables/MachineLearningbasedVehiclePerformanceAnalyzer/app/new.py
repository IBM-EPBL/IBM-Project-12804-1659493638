import requests
import json

API_KEY = "XMGyyPuQidd9AY75a3we-PvLGeJ8Wyck7wmts7XiJVK4"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,
                                                                                 "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["cylinder", "displacement", "horsepower",
                                              "weight", "a", "my", "ori"]],
                                   "values": [[0.31188164, 0.07178791, -0.51345822, -0.00839082, 0.07769265,
                                               0.51815083, -0.72739454]]}]}

response_scoring = requests.post(
    'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e4882d87-eacf-4877-846a-c170a77ca63d/predictions?version=2022-11-18',
    json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
predictions = response_scoring.json()
pre = predictions['predictions'][0]['values'][0][0]
if(pre > 15):
 print("It is in a good condition")
else:
    print("Not in a good condition")