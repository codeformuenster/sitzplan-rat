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

    # Read seats config
    members = []
    with open('config-members.json') as f:
        members = json.load(f)

    seats = {}
    for member in members:
        seats[member.get('seat')] = member

    html = '<html><style> div {width:10%;height:80px;border:2x solid #eee} div.occ {border: 2px solid black} div.row {width:100%;border: 1px solid #ccc;clear: left;overflow: hidden;} div.row > div {float:left}</style><body>'

    sitzplanRows = config.get('roomLayout').get('rows')
    sitzplanCols = config.get('roomLayout').get('columns')

    for row in range(sitzplanRows):
        html = html + '<div class="row">'
        for column in range(sitzplanCols):
            seatId = '{}-{}'.format(row,column)
            personData = {}
            if seatId in seats:
                personData = seats[seatId]
                pName = personData.get('name')
                html = html + '<div class="occ">{}</div>'.format(pName if pName else '')
            else:
                html = html + '<div></div>'
        html = html + '</div>'

    html = html + '</body></html>'

    with open('sitzplan.html', 'w') as outfile:
        outfile.write(html)

    print(html)

if os.path.isfile(CONFIG_MEMBERS):
    print("Members config file exists.")
else:
    # Read Gremiuem (Rat)
    gremiumUrl = config.get('core').get('baseurl')
    LOGGER.debug("Base URL: %s", gremiumUrl)

    r = requests.get(gremiumUrl)
    gremium = r.json()

    print("Writing members file")
    getMembers(gremium.get('membership'))

writeSitzplanHtml()
