'''
THIS SCRIPT NOTIFIES THE I18N-CHANNEL WHEN A COMPONENT IS LOCKED
'''
import wlc
import apikey
import json
import requests

projects={'mobile':{},'server':{},'webapp':{},'desktop':{},'glossary':{}}
projects['mobile']['shipped']='mattermost-mobile_master'
projects['server']['shipped']='mattermost-server_master'
projects['webapp']['shipped']='mattermost-webapp_master'
projects['desktop']['shipped']='mattermost-desktop'
projects['glossary']['shipped']='glossary'

w=wlc.Weblate(apikey.myAPIKey)
current_locks={}
previous_locks= json.load(open("locks.txt"))

for project in projects:
  current_lock=w.get('https://translate.mattermost.com/api/components/mattermost/'+projects[project]['shipped']+'/lock/')
  current_locks[projects[project]['shipped']]=current_lock['locked']
  if (previous_locks[projects[project]['shipped']]!=current_lock['locked']):
    print("LOCKED/UNLOCKED")
    values = '{ "text": "# Shipped Languages '+projects[project]['shipped']+' is unlocked now in Weblate "}'
    if current_lock['locked']==True:
      values = '{ "text": "# Shipped Languages '+projects[project]['shipped']+' is locked now in Weblate "}'
    try:
      headers = {'Content-Type': 'application/json',}
      print(values)
      response = requests.post(apikey.communityWebhook,headers=headers,data=values)
    except:
      print ('')
    finally:
      print('')
json.dump(current_locks,open("locks.txt",'w'))