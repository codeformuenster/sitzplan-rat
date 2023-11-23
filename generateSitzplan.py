# -*- coding: UTF-8 -*-

import re
import json
import logging
import requests
import os.path

from datetime import datetime, timedelta
from jinja2 import FileSystemLoader, Environment

# Basic logger configuration
logging.basicConfig(
    level=logging.DEBUG, format="<%(asctime)s %(levelname)s> %(message)s"
)
LOGGER = logging.getLogger(__name__)
TODAY = datetime.now()
LOGGER.info("=====> CHECK START %s <=====", TODAY)
DEFAULT_CONFIG_MEMBERS = "config-members.json"


# Read core config
data = []
with open("config-core.json") as f:
    config = json.load(f)

print(config)


def getMembers(oparlMembers):

    ## READ ALL MEMBERS FROM OPARL
    ## AND WRITE config-members.json

    currentDate = "{0}-{1:02d}-{2:02d}".format(TODAY.year, TODAY.month, TODAY.day)
    members = []

    for memberUrl in oparlMembers:

        # read membership json from oparl
        mrq = requests.get(memberUrl)
        oparlMember = mrq.json()
        startDate = oparlMember.get("startDate")
        endDate = oparlMember.get("endDate")
        personUrl = oparlMember.get("person")

        if not (startDate and currentDate):
            LOGGER.warning("missing date: %s - %s", startDate, endDate)
            isCurrentMember = (not endDate) or (endDate > currentDate)
        else:
            isCurrentMember = (startDate < currentDate) and (
                (not endDate) or (endDate > currentDate)
            )
        LOGGER.debug(
            "%s - %s -- isCurrent: %s -- %s",
            startDate,
            endDate,
            isCurrentMember,
            personUrl,
        )

        if isCurrentMember:
            # read person json from oparl
            prq = requests.get(personUrl)
            oparlPerson = prq.json()

            pid = 0
            matchObj = re.search(r"/(\d+)$", personUrl)
            if matchObj:
                pid = matchObj.group(1)

            name = oparlPerson.get("name")
            oparlEmail = oparlPerson.get("email")
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
                "seat": "",
            }
            LOGGER.debug("==> CURRENT MEMBER: %s", member)

            members.append(member)

    with open(DEFAULT_CONFIG_MEMBERS, "w") as outfile:
        json.dump(members, outfile)


def renderJinjaTemplate(directory, template_name, **kwargs):
    # Use Jinja2 Template engine for HTML generation
    # Source: https://daniel.feldroy.com/posts/jinja2-quick-load-function
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def getHtmlFilename(filename):
    return (
        "index.html"
        if filename == DEFAULT_CONFIG_MEMBERS
        else filename.replace(".json", ".html")
    )


def getNavLinks(selectedFile):
    nav = ""
    for seatingConfig in config.get("files"):
        nav = nav + '<a class="nav{}" href="{}">{}</a>'.format(
            (" active" if seatingConfig.get("file") == selectedFile else ""),
            getHtmlFilename(seatingConfig.get("file")),
            seatingConfig.get("date"),
        )
    return nav


def writeSitzplanHtml(seatingConfig):

    # Read seats config
    filename = seatingConfig.get("file")
    subTitle = seatingConfig.get("date") + " " + seatingConfig.get("room")
    members = []
    with open(filename) as f:
        members = json.load(f)

    seats = {}
    for member in members:
        seats[member.get("seat")] = member

    sitzplanRows = seatingConfig.get("rows")
    sitzplanCols = seatingConfig.get("columns")

    sitzplan = ""
    for row in range(sitzplanRows):
        sitzplan = sitzplan + '<div class="row">'
        for column in range(sitzplanCols):
            seatId = "{}-{}".format(row, column)
            personData = {}
            if seatId in seats:
                personData = seats[seatId]
                imageUrl = "https://www.stadt-muenster.de/sessionnet/sessionnetbi/im/pe{}.jpg".format(personData.get("pid"))
                imageAlt = personData.get("photo_url")
                photoSource = ""
                if imageAlt:
                    LOGGER.info("Found alt image: '%s' ", imageAlt)
                    imageUrl = imageAlt
                    photoSource = '{} ({} am {})</a>'.format(
                        personData.get("photo_source"),
                        personData.get("photo_link"),
                        personData.get("photo_link_date")
                    )
                pName = personData.get("name")
                sitzplan = (
                    sitzplan
                    + '<div data-id="{}" data-psrc="{}" data-party="{}" data-photo="{}" class="occ p-{}" style="{}"><span class="name">{}</span></div>'.format(
                        personData.get("pid"),
                        photoSource,
                        personData.get("party"),
                        imageUrl,
                        personData.get("party"),
                        "background-image: url({});".format(imageUrl),
                        pName if pName else "",
                    ) + "\n"
                )
            else:
                sitzplan = sitzplan + "<div></div>"
        sitzplan = sitzplan + "</div>"

    templateData = {
        "TITLE": config.get("info").get("title"),
        "SUBTITLE": subTitle,
        "NAV_LINKS": getNavLinks(filename),
        "DISCLAIMER": config.get("info").get("disclaimer"),
        "IMPRINT": config.get("info").get("imprint"),
        "LOGO": config.get("info").get("logo"),
        "SITZPLAN": sitzplan,
    }
    html = renderJinjaTemplate("template", "main.jinja2", **templateData)

    with open(getHtmlFilename(filename), "w") as outfile:
        outfile.write(html)

    # print(html)


if os.path.isfile(DEFAULT_CONFIG_MEMBERS):
    print("Default members config file exists.")
else:
    # Read Gremiuem (Rat)
    gremiumUrl = config.get("oparl").get("baseurl")
    LOGGER.debug("Base URL: %s", gremiumUrl)

    r = requests.get(gremiumUrl)
    gremium = r.json()

    print("Writing members file")
    getMembers(gremium.get("membership"))

for seatingConfig in config.get("files"):
    writeSitzplanHtml(seatingConfig)
