# ENDPOINTS
# factions https://elitebgs.app/api/ebgs/v5/factions?<params>
# systems https://elitebgs.app/api/ebgs/v5/systems?<params>
# stations https://elitebgs.app/api/ebgs/v5/stations?<params>
# ticks https://elitebgs.app/api/ebgs/v5/ticks?<params>
from __future__ import annotations

import requests
from pprint import pprint

from apimodules.elitebgs import model


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

payloads = {'faction': 'Alliance Rapid-reaction Corps'}
r = requests.get(sysend, params=payloads)
rdata = r.json()

response = model.EBGSSystemsPageV5(**rdata)

splitter = "---------------------------"

pprint(response.dict())
pprint(splitter)
for i in response.docs:
    pprint(i.name)
    pprint(splitter)
