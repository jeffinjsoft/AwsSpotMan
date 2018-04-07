# AwsSpotMan
django + boto3 + spot instance


# setup
- git clone https://github.com/jeffinjsoft/AwsSpotMan.git
- cd AwsSpotMan
- pip install -r requirement.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver


For intial setup you need to get all values from aws with accont id :- python manage.py refresh_values --check=all --accnt='xxxxxxxxx'
and set schedule check cron in every minute ( * * * * * python manage.py check_schedule )

### Usage
- Run Server :- python manage.py runserver
- Custom command :- python manage.py refresh_values --check=all --accnt='xxxxxxxxx'
- cron command :- python manage.py check_schedule ( every minute )
