'''
THIS SCRIPT NOTIFIES THE I18N-CHANNEL WHEN A COMPONENT IS LOCKED
'''
import wlc
import apikey
import json
import requests
from requests.exceptions import HTTPError
from datetime import datetime
import datetime as DT

projects={'mobile':{},'server':{},'webapp':{},'desktop':{},'glossary':{}}
projects['mobile']='mattermost/mattermost-mobile-v2'
projects['server']='mattermost/mattermost-server_master'
projects['webapp']='mattermost/mattermost-webapp_master'
projects['desktop']='mattermost/mattermost-desktop'
projects['focalboard']='focalboard/webapp'
projects['playbooks']='playbooks/webapp'
projects['glossary']='mattermost/glossary'

mention={}
mention['mobile']='cc: @guillermo.vaya , @pantelis.vratsalis'
mention['server']='cc: @guillermo.vaya , @pantelis.vratsalis'
mention['webapp']='cc: @guillermo.vaya , @pantelis.vratsalis'
mention['desktop']='cc: @devin.binnie'
mention['focalboard']='cc: @jesus.espino , @scott.bishel'
mention['playbooks']='cc: @jesse.hallam , @caleb.roseland'
mention['glossary']=''

w=wlc.Weblate(key=apikey.myAPIKey)
current_locks={}
previous_locks= json.load(open("locks.txt"))

def notificateChannel(project,current_lock):
  values = '{ "text": "#### Shipped Languages '+projects[project]+' is unlocked now in Weblate '+mention[project]+' "}'
  if current_lock['locked']==True:
    values = '{ "text": "##### Shipped Languages '+projects[project]+' is locked now in Weblate '+mention[project]+' "}'
  try:
    headers = {'Content-Type': 'application/json',}
    current_locks[projects[project]]=current_lock
    current_locks[projects[project]+"-channel_notified"]=now
    print("locked sent")
    response = requests.post(apikey.communityWebhook,headers=headers,data=values)
    response.raise_for_status()
  except HTTPError as http_err:
    print(f'HTTP error occurred while notifying Mattermost-channel: {http_err}')
  except Exception as err:
    print(f'Other error occurred while notifying Mattermost-channel: {err.message} {err.args}')
  else:
    print('Success!')

for project in projects:
  now=datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
  print(now)
  current_lock=w.get('https://translate.mattermost.com/api/components/'+projects[project]+'/lock/')
  current_locks[projects[project]]=current_lock
  if (previous_locks[projects[project]]!=current_lock):
    print("SENT NOTIFICICATION CAUSE LOCK HAS CHANGED")
    notificateChannel(project,current_lock)
    current_locks[projects[project]+"-channel_notified"]=now
  else:
    previous_notification = datetime.strptime(previous_locks[projects[project]+"-channel_notified"], '%Y-%m-%d, %H:%M:%S')
    current_locks[projects[project]+"-channel_notified"]=previous_locks[projects[project]+"-channel_notified"]
    if (datetime.now()-DT.timedelta(days=7))>previous_notification and current_lock['locked']:
      print("reminder for "+str(projects[project]))
      notificateChannel(project,current_lock)
      current_locks[projects[project]+"-channel_notified"]=now
json.dump(current_locks,open("locks.txt",'w'))
