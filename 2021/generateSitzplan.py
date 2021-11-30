# -*- coding: UTF-8 -*-

import re
import json
import logging
import requests
import os.path

from datetime import datetime, timedelta

# Basic logger configuration
logging.basicConfig(level=logging.DEBUG, format='<%(asctime)s %(levelname)s> %(message)s')
LOGGER = logging.getLogger(__name__)
TODAY = datetime.now()
LOGGER.info("=====> CHECK START %s <=====", TODAY)
CONFIG_MEMBERS = 'config-members.json'


# Read core config
data = []
with open('config-core.json') as f:
    config = json.load(f)

print(config)

# Read Gremiuem (Rat)
gremiumUrl = config.get('core').get('baseurl')
LOGGER.debug("Base URL: %s", gremiumUrl)

r = requests.get(gremiumUrl)
gremium = r.json()

def getMembers(oparlMembers):

    ## READ ALL MEMBERS FROM OPARL
    ## AND WRITE config-members.json

    currentDate = '{0}-{1:02d}-{2:02d}'.format(TODAY.year, TODAY.month, TODAY.day)
    members = []

    for memberUrl in oparlMembers:

        # read membership json from oparl
        mrq = requests.get(memberUrl)
        oparlMember = mrq.json()
        startDate = oparlMember.get('startDate')
        endDate = oparlMember.get('endDate')
        personUrl = oparlMember.get('person')

        isCurrentMember = (startDate < currentDate) and ((not endDate) or (endDate > currentDate))
        LOGGER.debug("%s - %s -- isCurrent: %s -- %s", startDate, endDate, isCurrentMember, personUrl)

        if isCurrentMember:
            # read person json from oparl
            prq = requests.get(personUrl)
            oparlPerson = prq.json()

            pid = 0
            matchObj = re.search( r'/(\d+)$', personUrl)
            if matchObj:
                pid = matchObj.group(1)

            name = oparlPerson.get('name')
            oparlEmail = oparlPerson.get('email')
            email = ""
            party = ""
            if oparlEmail:
                email = oparlEmail.pop()
            if "cdu" in email.lower():
                party = "CDU"
            elif "volt" in email.lower():
                party = "VOLT"
            elif "gruene" in email.lower():
                party = "GRÜNE"
            elif "spd" in email.lower():
                party = "SPD"

            member = {
                "name": name,
                "pid": pid,
                "party": party,
                "email": email,
                "seat": ""
            }
            LOGGER.debug("member %s", member)

            members.append(member)


    with open(CONFIG_MEMBERS, 'w') as outfile:
        json.dump(members, outfile)


def writeSitzplanHtml():
    html = '<html><body>'



if os.path.isfile(CONFIG_MEMBERS):
    print("Members config file exists.")
else:
    print("Writing members file")
    getMembers(gremium.get('membership'))


