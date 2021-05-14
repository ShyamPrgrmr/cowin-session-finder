# COWIN NOTIFIER

This python script will help one to get notification on email whenever slots are available on the cowin app.
Cowin api are used to do all perpose.

## status : 
    1. working on frontend making and multiple user accessability
    2. sns ( text messaging )
    3. working on sockets

## Requirement, packages and Installation : 
    1. You Need to have EC2 (Any Linux Distro) in amazon 
    2. Install and configure AWS CLI (Setting access id and access key *get_this_from_aws_credential_ses*)
    3. Python 3.8
    4. Python Packages boto3 (AWS SDK), Requests package
    5. Before sending mail you need to add mail into ses just run initmail.py for once. and you will get mail. you can do it manually
    6. Clone this repository
    7. do changes in config.json ( email:*sender_mail*,config_email:*configuration_mail*,districtid:*your_district_id*)
        email :: is your sender email address
        config_email :: this email for configuration as well as receiver email
        (both can be same)
        districtid :: Check it on cowin api. Initially set for amravati.
    8. 


   
