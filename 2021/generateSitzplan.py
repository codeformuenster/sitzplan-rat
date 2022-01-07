# -*- coding: UTF-8 -*-

import re
import json
import logging
import requests
import os.path

from datetime import datetime, timedelta
from jinja2 import FileSystemLoader, Environment

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


def renderJinjaTemplate(directory, template_name, **kwargs):
    # Use Jinja2 Template engine for HTML generation
    # Source: https://daniel.feldroy.com/posts/jinja2-quick-load-function
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def writeSitzplanHtml():

    # Read seats config
    members = []
    with open('config-members.json') as f:
        members = json.load(f)

    seats = {}
    for member in members:
        seats[member.get('seat')] = member

    sitzplanRows = config.get('roomLayout').get('rows')
    sitzplanCols = config.get('roomLayout').get('columns')

    sitzplan = ""
    for row in range(sitzplanRows):
        sitzplan = sitzplan + '<div class="row">'
        for column in range(sitzplanCols):
            seatId = '{}-{}'.format(row,column)
            personData = {}
            if seatId in seats:
                personData = seats[seatId]
                pName = personData.get('name')
                sitzplan = sitzplan + '<div data-id="{}" data-party="{}" class="occ p-{}" style="{}"><span class="name">{}</span></div>'.format(
                    personData.get('pid'),
                    personData.get('party'),
                    personData.get('party'),
                    'background-image: url(https://www.stadt-muenster.de/sessionnet/sessionnetbi/im/pe{}.jpg);'.format(personData.get('pid')),
                    pName if pName else ''
                    )
            else:
                sitzplan = sitzplan + '<div></div>'
        sitzplan = sitzplan + '</div>'

    templateData = {
        "TITLE": config.get('info').get('title'),
        "DATE": config.get('info').get('date'),
        "DISCLAIMER": config.get('info').get('disclaimer'),
        "IMPRINT": config.get('info').get('imprint'),
        "LOGO": config.get('info').get('logo'),
        "SITZPLAN": sitzplan
    }
    html = renderJinjaTemplate("template", "main.jinja2", **templateData)

    with open('sitzplan.html', 'w') as outfile:
        outfile.write(html)

    print(html)

if os.path.isfile(CONFIG_MEMBERS):
    print("Members config file exists.")
else:
    # Read Gremiuem (Rat)
    gremiumUrl = config.get('oparl').get('baseurl')
    LOGGER.debug("Base URL: %s", gremiumUrl)

    r = requests.get(gremiumUrl)
    gremium = r.json()

    print("Writing members file")
    getMembers(gremium.get('membership'))

writeSitzplanHtml()
