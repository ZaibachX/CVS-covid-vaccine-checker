'''
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install beepy

in your terminal.
'''
import requests
import time
import beepy
import smtplib
import ssl
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def load_env(): ###Update the .env.yml file with your information and save as env.yml (No period in front)
    env = yaml.safe_load(open('env.yml'))

    return env

def send_email(user, pwd, email_address, email_to, body):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(user, pwd)
    message = 'Subject: {}\n\n{}'.format('CVS Vaccine - Available', body)
    s.sendmail(email_address,email_to,message)

def findAVaccine():
    hours_to_run = 3 ###Update this to set the number of hours you want the script to run.
    max_time = time.time() + hours_to_run*60*60
    while time.time() < max_time:

        state = 'CA' ###Update with your state abbreviation. Be sure to use all CAPS, e.g. RI

        response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo".format(state.lower()), 
                                headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
        payload = response.json()

        mappings = {}
        for item in payload["responsePayloadData"]["data"][state]:
            mappings[item.get('city')] = item.get('status')

        print(time.ctime())
        ###Update with your cities nearby
        cities = ['ALISO VIEJO',
                  'CARLSBAD',
                  'CHULA VISTA',
                  'ENCINITAS',
                  'ESCONDIDO',
                  'LA JOLLA',
                  'LA MESA',
                  'MURRIETA',
                  'NATIONAL CITY',
                  'OCEANSIDE',
                  'POWAY',
                  'RAMONA',
                  'SAN CLEMENTE',
                  'SAN DIEGO',
                  'SAN MARCOS',
                  'SANTEE',
                  'SOLANA BEACH',
                  'SPRING VALLEY',
                  'TEMECULA',
                  'VISTA']
        for city in cities:
            print(city, mappings[city])

        ### Created a dictionary to append multiple cities and send it out via gmail
        cities_dict = dict()
        for (key, value) in mappings.items():
            if (value == 'Available') and (key in cities):
                cities_dict[key] = value
            else:
                pass

        if len(cities_dict) > 0:
            beepy.beep(sound = 'coin')
            env = load_env()
            send_email(env['user'],
                            env['pwd'],
                            env['user'],
                            env['email_to'],
                            env['body'].format(', '.join(cities_dict.keys()))
                            )
            break ###Feel free to remove the break to have the script continually send an email (when a city is available) if you'd like

        time.sleep(60) ###This runs every 60 seconds. Update here if you'd like it to go every 10min (600sec)
        print('\n')

findAVaccine() ###this final line runs the function. Your terminal will output the cities every 60seconds