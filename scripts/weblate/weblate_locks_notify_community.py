'''
THIS SCRIPT NOTIFIES THE I18N-CHANNEL WHEN A COMPONENT IS LOCKED
'''
import wlc
import apikey
import json
import requests
from requests.exceptions import HTTPError


projects={'mobile':{},'server':{},'webapp':{},'desktop':{},'glossary':{}}
projects['mobile']='mattermost/mattermost-mobile_master'
projects['server']='mattermost/mattermost-server_master'
projects['webapp']='mattermost/mattermost-webapp_master'
projects['desktop']='mattermost/mattermost-desktop'
projects['focalboard']='focalboard/webapp'
projects['playbooks']='playbooks/webapp'
projects['glossary']='mattermost/glossary'

mention={}
mention['mobile']='cc: @guillermo.vaya,@zef.hemel'
mention['server']='cc: @guillermo.vaya,@zef.hemel'
mention['webapp']='cc: @guillermo.vaya,@zef.hemel'
mention['desktop']='cc: @devin.binnie'
mention['focalboard']='cc: @jesus.espino,@scott.bishel'
mention['playbooks']='cc: @jesse.hallam,@caleb.roseland'
mention['glossary']=''

w=wlc.Weblate(key=apikey.myAPIKey)
current_locks={}
previous_locks= json.load(open("locks.txt"))



for project in projects:
  current_lock=w.get('https://translate.mattermost.com/api/components/'+projects[project]+'/lock/')
  current_locks[projects[project]]=current_lock['locked']
  if (previous_locks[projects[project]]!=current_lock['locked']):
    print("LOCKED/UNLOCKED")
    values = '{ "text": "# Shipped Languages '+projects[project]+' is unlocked now in Weblate '+mention[project]+' "}'
    if current_lock['locked']==True:
      values = '{ "text": "# Shipped Languages '+projects[project]+' is locked now in Weblate '+mention[project]+' "}'
    try:
      headers = {'Content-Type': 'application/json',}
      print(values)
      response = requests.post(apikey.communityWebhook,headers=headers,data=values)
      response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred while notifying Mattermost-channel: {http_err}')
    except Exception as err:
        print(f'Other error occurred while notifying Mattermost-channel: {err.message} {err.args}')
    else:
        print('Success!')
json.dump(current_locks,open("locks.txt",'w'))
