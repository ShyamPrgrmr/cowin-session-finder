import boto3
from botocore import config
from botocore.exceptions import ClientError
import datetime as dt
import requests
import sys
import json
from datetime import datetime

with open('config.json') as json_file:
    config = json.load(json_file)
    email = config['email']
    rec = config['config_email']

print("Sender Email ",email)
print("Receiver Email ",rec)
print("Checking Slots for ",config['districtid'])

def send_email_ses(body,sub):
    SENDER = email
    RECIPIENT = rec
    AWS_REGION = "ap-south-1"
    SUBJECT = sub
    BODY_HTML = body

    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def storedata():
    pass



def check_for_slots():
    send = False
    index = 0
    index = index + 1
    today = dt.date.today()
    y = today.year
    m = today.month
    d = today.day
    date = str(d+1)+"-"+str(m)+"-"+str(y)
    districtid=str( config['districtid'] ) #change district id
    try:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+districtid+"&date="+date
        payload={}
        user_agent = {'User-agent': 'Mozilla/5.0','accept':'application/json'}
        response = requests.request("GET", url, headers=user_agent, data=payload)
        data = response.json()
        
        if send:
            pass
        else:
            size = len(data['centers'])
            centers = data['centers']
            table_data=""

            for center in centers:
                name = center['name']
                address = center['address']
                pincode = center['pincode']
                fee_type = center['fee_type']
                vaccine_type = center['sessions'][0]['vaccine']
                number_of_vaccine = center['sessions'][0]['available_capacity']
                for_age = center['sessions'][0]['min_age_limit']
                if number_of_vaccine > 0:
                    table_data += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{address}</td>
                            <td>{pincode}</td>
                            <td>{number_of_vaccine}</td>
                            <td>{vaccine_type}</td>
                            <td>{fee_type}</td>
                            <td>{for_age}</td>
                        </tr>
                    """
                    send=True

            
            
            table = f"""
                <h1>List of all available vaccines</h1>
                <h4>Total Center found : {size}</h4>
                <br>
                <table border='1'>
                    
                    <thead>
                        <th>Center name</th>
                        <th>Center Address</th>
                        <th>Center Pincode</tr>
                        <th>Available Vaccines</th>
                        <th>Vaccinne Type</th>
                        <th>Fee Type</th>
                        <th>For Age</th>
                    </thead>

                    <tbody>
                        {table_data}
                    </tbody>

                </table>

                <small>Bot is turned off start it manually</small>
            """
            if(table_data != ""):
                print("Sending Mail....")
                send_email_ses(table,"Available Vaccination Slots")
                print("Mail Sent")
                return True
            else:
                return False
            
    except Exception as e:
        print("error "+e.__str__)
        

now = datetime.now()
h = int(now.strftime("%H"))
m = int(now.strftime("%M"))


with open('data.json') as json_file:
    content = json.load(json_file)
    updated = int(content['updated'])
    timeset = int(content['timeset'])
    if(timeset == 0):
        
        content['time']['hour'] = h
        content['time']['minute'] = m
        content['timeset'] = 1

        with open('data.json', 'w') as outfile:
            json.dump(content, outfile)
        
if(updated==0):
    if(check_for_slots()):
        content['updated'] = 1
        with open('data.json', 'w') as outfile:
                json.dump(content, outfile)
        print("Slots Available")
    else:
        print("Slots Not Available")
else:
    print("Already Updated")
    if(content['timeset']==1):
        hour = content['time']['hour']
        mint = content['time']['minute']
        if(hour<h):
            print("Can Be Updated")
            print("Setting new Time")
            content['updated'] = 0 
            content['time']['hour'] = h
            content['time']['minute'] = m
            content['timeset'] = 1
            print("New Time "+str(h)+":"+str(m))
            with open('data.json', 'w') as outfile:
                json.dump(content, outfile)