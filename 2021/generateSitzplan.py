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

    sitzplanRows = config.get('roomLayout').get('rows')
    sitzplanCols = config.get('roomLayout').get('columns')

    html = '''<!doctype html><html lang="de">
        <meta charset="utf-8">
        <style>
            div {{width:{}%;height:70px;border:2x solid #eee}}
            div.row {{width:100%;border: 1px solid #fefefe;clear: left;}}
            div.row > div {{float:left}}
            .p-GRÜNE {{background-color:#3f3}}
            .p-LINKE {{background-color:#f39}}
            .p-VOLT {{background-color:#502379;color:white}}
            .p-ÖDP {{background-color:#ff6400}}
            .p-AFD {{background-color:#09f}}
            .p-CDU {{background-color:#000;color:white}}
            .p-SPD {{background-color:#f33}}
            .p-OHNE {{color:white;background: repeating-linear-gradient(
                45deg,
                #606dbc,
                #606dbc 10px,
                #465298 10px,
                #465298 20px
                );}}
            #member img {{
                max-width:150px;
                max-height:200px;
             }}
            #member {{
                display:block;
                position:absolute;
                overflow:hidden;
                background-color:yellow;
                border: 1px solid black;
                border-radius: 5px;
                width: 200px;
                text-align: center;
                height: 260px;
            }}
            #member span {{
                background-color: orange;
                display: block;
                padding: 4px 0;
            }}
            .occ {{
                overflow:hidden;
                border: 1px solid black;
                cursor: pointer;
                border-radius: 7px;
                margin: 0 1px 0 0;
            }}
            div.occ span {{
                margin: 4px 4px 0 4px;
                display: inline-block;
                font-size: 10pt;
                overflow-wrap:break-word;
            }}
        </style>
        <script src="https://code.jquery.com/jquery-3.5.0.js"></script>
        <body>
        '''.format(7)

    for row in range(sitzplanRows):
        html = html + '<div class="row">'
        for column in range(sitzplanCols):
            seatId = '{}-{}'.format(row,column)
            personData = {}
            if seatId in seats:
                personData = seats[seatId]
                pName = personData.get('name')
                html = html + '<div data-id="{}" data-party="{}" class="occ p-{}"><span class="name">{}</span>{}</div>'.format(
                    personData.get('pid'),
                    personData.get('party'),
                    personData.get('party'),
                    pName if pName else '',
                    personData.get('seat')
                    )
            else:
                html = html + '<div></div>'
        html = html + '</div>'

    html = html + '''
        <div id="member">
            <span class="name">Max Muster</span>
            <span class="party">Party</span>
            <img class="photo" src="url" />
        </div>
        <script>
            var errCount = 0;
            $("#member .photo").on('error', function(e) {
                event.stopPropagation();
                if (errCount++ <= 1) {
                    $("#member .photo").attr("src", "img/person.png");
                }
            });
            $("div.occ").click(function(event){
                const pid = $(this).data("id");
                location.href="https://www.stadt-muenster.de/sessionnet/sessionnetbi/pe0051.php?__kpenr="+pid;
            }).hover(function(event) {
                errCount = 0;
                const pid = $(this).data("id");
                const name = $(this).find(".name").text();
                const party = $(this).data("party");
                const photoUrl = 'https://www.stadt-muenster.de/sessionnet/sessionnetbi/im/pe'+pid+'.jpg'
                console.log("id", pid);
                $("#member .name").html(name);
                $("#member .party").html(party);
                $("#member .photo").attr("src", photoUrl);
                $("#member").css({top: event.clientY, left: event.clientX}).show();
            }, function() {
                $("#member").hide();
            });
        </script>
        </body></html>
        '''

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
