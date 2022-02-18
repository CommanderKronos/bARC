# ENDPOINTS
# factions https://elitebgs.app/api/ebgs/v5/factions?<params>
# systems https://elitebgs.app/api/ebgs/v5/systems?<params>
# stations https://elitebgs.app/api/ebgs/v5/stations?<params>
# ticks https://elitebgs.app/api/ebgs/v5/ticks?<params>
from typing import Tuple

import requests
from pprint import pprint
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from modules.elitebgs import model
from helpers import sqlite

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
SYSTEMS_PARAMS = ['id', 'eddbid', 'name', 'allegiance', 'government', 'state', 'primaryEconomy', 'secondaryEconomy',
                  'faction', 'factionId', 'factionControl', 'security', 'activeState', 'pendingState',
                  'recoveringState', 'influenceGT', 'influenceLT', 'factionAllegiance', 'factionGovernment',
                  'referenceSystem', 'referenceSystemID', 'referenceDistance', 'referenceDistanceMin', 'sphere',
                  'beginsWith', 'minimal', 'factionDetails', 'factionHistory', 'timeMin', 'timeMax', 'count', 'page']

sysend = 'https://elitebgs.app/api/ebgs/v5/systems'
facend = 'https://elitebgs.app/api/ebgs/v5/factions'
statend = 'https://elitebgs.app/api/ebgs/v5/stations'
ticksend = 'https://elitebgs.app/api/ebgs/v5/ticks'

splitter = "---------------------------"


def validate_sys_params(params: tuple) -> Tuple[bool, str]:
    for param in params:
        if param not in SYSTEMS_PARAMS:
            return False, param
    return True, 'none'


def system_lookup() -> model.EBGSSystemsPageV5:
    pass


def basic_system_lookup(system_name: str):
    """Lookup system information based on name with EliteBGS API"""
    payloads = {'name': system_name}
    data = model.EBGSSystemsPageV5(**requests.get(sysend, params=payloads).json())
    system = data.docs[0]
    return {'system_id': system.id, 'eddbid': system.eddb_id, 'name': system.name, 'x': system.x, 'y': system.y,
            'z': system.z}


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


def conflict_pic_gen(conflicts: dict, system: str):
    fig, ax = plt.subplots()
    table_data = []
    for conflict in conflicts[system]:
        table_data.append(["Type:", "Participants:", "Stakes:", "Days won:"])
        table_data.append([conflict['type'], conflict['party1'], conflict['stake1'], conflict['dayswon1']])
        table_data.append(['           ', conflict['party2'], conflict['stake2'], conflict['dayswon2']])

        # table_data.append(["Type:", conflict['type'], '           '])
        # table_data.append(["Participants:", conflict['party1'], conflict['party2']])
        # table_data.append(["Stakes:", conflict['stake1'], conflict['stake2']])
        # table_data.append(["Status:", conflict['dayswon1'], conflict['dayswon2']])
    # table = ax.table(cellText=table_data, loc='best')
    # ax.axis('off')
    # plt.axis('off')
    fig = go.Figure(data=[go.Table(cells=dict(values=table_data))])
    # fig.update_layout(width=500, height=300)
    fig.write_image('temp/conflicttable.png')


def bgsreport():
    """Return """
    monitored_systems = sqlite.monitoredsystems()
    data = {}
    conflicts = {}
    previoustick = getprevioustick()
    timeMin = unix_time_millis(previoustick - timedelta(hours=2))
    timeMax = unix_time_millis(previoustick + timedelta(hours=2))

    for system in monitored_systems:
        payloads = {'name': system, 'factionHistory': 'true', 'factionDetails': 'true', 'timeMin': timeMin,
                    'timeMax': timeMax}
        response = requests.get(sysend, params=payloads)
        r = model.EBGSSystemsPageV5(**response.json())
        for doc in r.docs:
            data[doc.name] = []
            conflicts[doc.name] = []
            history = doc.faction_history
            infhistory = {}

            for conflict in doc.conflicts:
                conflicts[doc.name].append(
                    {'type': conflict.type, 'party1': conflict.faction1.name, 'stake1': conflict.faction1.stake,
                     'dayswon1': conflict.faction1.days_won, 'party2': conflict.faction2.name,
                     'stake2': conflict.faction2.stake, 'dayswon2': conflict.faction2.days_won}
                )

            # Get Influence history
            for old_faction in history:
                infhistory[old_faction.faction_name] = old_faction.influence
            # Get current influence and other data
            for faction in doc.factions:
                faction_presence = faction.faction_details.faction_presence
                states = faction_presence.getallstates()
                newinf = faction_presence.influence

                # Add logic to split the state definition if it exists out of two words or more
                for state_type in states.keys():
                    for state_index in range(len(states[state_type])):
                        states[state_type][state_index] = states[state_type][state_index][0].upper() + states[state_type][state_index][1:]

                if faction.name in infhistory.keys():
                    oldinf = infhistory[faction.name]
                else:
                    oldinf = newinf
                infchange = newinf - oldinf

                # add last update time
                data[doc.name].append(
                    {'name': faction.name, 'influence': newinf,
                     'active': states['active'], 'pending': states['pending'],
                     'recovering': states['recovering'], 'conflicts': faction_presence.conflicts,
                     'infchange': infchange})
    return data, conflicts
