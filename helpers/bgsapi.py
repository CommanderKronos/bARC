# ENDPOINTS
# factions https://elitebgs.app/api/ebgs/v5/factions?<params>
# systems https://elitebgs.app/api/ebgs/v5/systems?<params>
# stations https://elitebgs.app/api/ebgs/v5/stations?<params>
# ticks https://elitebgs.app/api/ebgs/v5/ticks?<params>

import requests
from pprint import pprint
from datetime import datetime, timedelta

from apimodules.elitebgs import model
from helpers import sqllite

# All different types of paramaters for every endpoint.

BODIES_PARAMS = ['eddbid', 'name', 'materials', 'systemname', 'reservetypename', 'ispopulated', 'power', 'ringtypename',
                 'bodygroupname', 'hasrings', 'bodytypename', 'distancearrival', 'ismainstar', 'specclass', 'lumoclass',
                 'landable', 'page']
FACTIONS_PARAMS = ['eddbid', 'name', 'allegiancename', 'governmentname', 'playerfaction', 'power', 'homesystemname',
                   'page']
POPULATEDSYSTEMS_PARAMS = ['eddbid', 'systemaddress', 'name', 'allegiancename', 'governmentname', 'statenames',
                           'primaryeconomyname', 'power', 'powerstatename', 'permit', 'securityname', 'factionname',
                           'presencetype', 'page']
STATIONS_PARAMS = ['eddbid', 'marketid', 'name', 'ships', 'moduleid', 'controllingfactionname', 'statenames',
                   'allegiancename', 'governmentname', 'minlandingpad', 'distancestar', 'facilities', 'commodities',
                   'stationtypename', 'planetary', 'economyname', 'permit', 'power', 'powerstatename', 'systemname',
                   'page']
SYSTEMS_PARAMS = ['eddbid', 'systemaddress', 'name', 'allegiancename', 'governmentname', 'primaryeconomyname', 'power',
                  'powerstatename', 'permit', 'securityname', 'page']

sysend = 'https://elitebgs.app/api/ebgs/v5/systems'
facend = 'https://elitebgs.app/api/ebgs/v5/factions'
statend = 'https://elitebgs.app/api/ebgs/v5/stations'
ticksend = 'https://elitebgs.app/api/ebgs/v5/ticks'

# payloads = {'faction': 'Alliance Rapid-reaction Corps'}
# r = requests.get(sysend, params=payloads)
# rdata = r.json()
#
# response = model.EBGSSystemsPageV5(**rdata)
#
# splitter = "---------------------------"
#
# pprint(response.dict())
# pprint(splitter)
# for i in response.docs:
#     pprint(i.name)
#     pprint(splitter)
splitter = "---------------------------"


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    dt = dt.replace(tzinfo=None)
    return (dt - epoch).total_seconds() * 1000.0


def getprevioustick():
    """Get the time of the previous tick (the tick before the most recent one)"""
    lasttick = getlasttick()
    maxTime = unix_time_millis(lasttick)
    minTime = unix_time_millis(lasttick - timedelta(hours=26))
    rdata = requests.get(ticksend, params={'timeMin': minTime, 'timeMax': maxTime}).json()
    rdata[0]['time'] = rdata[0]['time'].replace("Z", '+00:00')
    data = model.TickTimesV5(**rdata[0])
    return datetime.fromisoformat(data.time)


def getlasttick():
    """Get the time of the most recent tick"""
    rdata = requests.get(ticksend).json()
    rdata[0]['time'] = rdata[0]['time'].replace("Z", '+00:00')
    data = model.TickTimesV5(**rdata[0])
    return datetime.fromisoformat(data.time)


def bgsreport():
    """Return """
    monitored_systems = sqllite.monitoredsystems()
    data = {}
    previoustick = getprevioustick()
    timeMin = unix_time_millis(previoustick - timedelta(hours=2))
    timeMax = unix_time_millis(previoustick + timedelta(hours=2))
    conflicts = {}
    for system in monitored_systems:
        payloads = {'name': system, 'factionHistory': 'true', 'factionDetails': 'true', 'timeMin': timeMin,
                    'timeMax': timeMax}
        response = requests.get(sysend, params=payloads)
        r = model.EBGSSystemsPageV5(**response.json())
        for doc in r.docs:
            data[doc.name] = []
            history = doc.faction_history
            infhistory = {}

            for old_faction in history:
                infhistory[old_faction.faction_name] = old_faction.influence
            for faction in doc.factions:
                faction_presence = faction.faction_details.faction_presence
                states = faction_presence.getallstates()
                newinf = faction_presence.influence

                if faction.name in infhistory.keys():
                    oldinf = infhistory[faction.name]
                else:
                    oldinf = newinf
                infchange = "{0:.2%}".format(newinf - oldinf)

                for conflict in faction_presence.conflicts:
                    conflicts[conflict.opponent_name] = {'stake': conflict.stake, 'system': system}

                # add last update time
                data[doc.name].append(
                    {'name': faction.name, 'influence': "{0:.2%}".format(newinf),
                     'active': states['active'], 'pending': states['pending'],
                     'recovering': states['recovering'], 'conflicts': faction_presence.conflicts,
                     'infchange': infchange})
    return data, conflicts
