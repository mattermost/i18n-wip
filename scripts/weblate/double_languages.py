

import wlc
import apikey
import requests
import math
import json
from requests.exceptions import HTTPError


w=wlc.Weblate(apikey.myAPIKey)
projects={'mobile':{},'server':{},'webapp':{},'glossary':{}}
projects['mobile']['shipped']='mattermost-mobile_master'
projects['mobile']['wip']='mattermost-mobile-wip'
projects['server']['shipped']='mattermost-server_master'
projects['server']['wip']='mattermost-server-wip'
projects['webapp']['shipped']='mattermost-webapp_master'
projects['webapp']['wip']='mattermost-webapp-wip'
projects['glossary']['shipped']='glossary'
projects['glossary']['wip']='glossary'
current_notification_state={"state":"false"}
previous_notification_state= json.load(open("./notification_state.txt"))

for project in projects:
  shippedLanguages={}
  WIPLanguages={}
### GETTING THE SHIPPED LANGUAGES ###
  #print('GETTING SHIPPED LANGUAGES FOR '+project)
  shippedProjects=w.get('https://translate.mattermost.com/api/components/mattermost/'+projects[project]['shipped']+'/translations/')
  for shippedLanguage in shippedProjects['results']:
    if shippedLanguage['language']['code']=='en':
      continue
    shippedLanguageCode=shippedLanguage['language']['code']
    shippedLanguageName=shippedLanguage['language']['name']
    shippedLanguages[shippedLanguageCode]=shippedLanguageName

  #print('GETTING WIP LANGUAGES FOR '+project)
  page=1
  next='https://translate.mattermost.com/api/components/i18n-wip/'+projects[project]['wip']+'/translations/'
  WIPProjects=w.get(next)
  lastpage=math.ceil(WIPProjects['count']/20)
  while page<=lastpage:   
    next='https://translate.mattermost.com/api/components/i18n-wip/'+projects[project]['wip']+'/translations/?page='+str(page)
    WIPProjects=w.get(next)
    page=page+1
    for WIPLanguage in WIPProjects['results']:
      if WIPLanguage['language']['code']=='en':
        continue
      WIPLanguageCode=WIPLanguage['language']['code']
      WIPLanguageName=WIPLanguage['language']['name']
      WIPLanguages[WIPLanguageCode]=WIPLanguageName

### GETTING REMOVING THE WIP LANGUAGES THAT ARE ALREADY IN SHIPPED ###
  for languageToRemove in shippedLanguages.keys() & WIPLanguages.keys():
    current_notification_state['state']="true"
    if (previous_notification_state['state']=="false"):
      try:
        headers = {'Content-Type': 'application/json',}
        values = '{ "text": "Hi @ctlaltdieliet and @carrie.warner: a shipped language is detected in WIP  ('+languageToRemove+') in this '+project+' This project is locked now"}'
        responseMattermost = requests.post(apikey.i18nWebhook,headers=headers,data=values)
        responseMattermost.raise_for_status()
      except HTTPError as http_err:
          print('HTTP error occurred while notifying Mattermost channel: '+http_err) 
      except Exception as err:
          print('Other error occurred while notifying Mattermost channel: '+err.message+' '+err.args)
      try:
          responseWeblate=w.request('post','https://translate.mattermost.com/api/components/i18n-wip/'+projects[project]['wip']+'/lock/',{'lock':True})
      except HTTPError as http_err:
          print('HTTP error occurred while locking '+projects[project]['wip']+': '+http_err) 
      except Exception as err:
          print('Other error occurred while locking : '+ projects[project]['wip']+' '+err.message+' '+err.args)
json.dump(current_notification_state,open("./notification_state.txt",'w'))
