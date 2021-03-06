# generated by datamodel-codegen:
#   filename:  api-docs.json
#   timestamp: 2022-02-14T13:59:03+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Model(BaseModel):
    __root__: Any


class EBGSAllEconomiesV5(BaseModel):
    name: Optional[str] = None
    proportion: Optional[int] = None


class EBGSConflictFactionV5(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    opponent_name: Optional[str] = None
    opponent_name_lower: Optional[str] = None
    opponent_faction_id: Optional[str] = None
    station_id: Optional[str] = None
    stake: Optional[str] = None
    stake_lower: Optional[str] = None
    days_won: Optional[int] = None


class EBGSConflictSystemFactionV5(BaseModel):
    faction_id: Optional[str] = None
    name: Optional[str] = None
    name_lower: Optional[str] = None
    station_id: Optional[str] = None
    stake: Optional[str] = None
    stake_lower: Optional[str] = None
    days_won: Optional[int] = None


class EBGSConflictSystemV5(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    faction1: Optional[EBGSConflictSystemFactionV5] = None
    faction2: Optional[EBGSConflictSystemFactionV5] = None


class EBGSNameAliasV5(BaseModel):
    name: Optional[str] = None
    name_lower: Optional[str] = None


class EBGSStateActiveV5(BaseModel):
    state: Optional[str] = None


class EBGSStateV5(BaseModel):
    state: Optional[str] = None
    trend: Optional[int] = None


class EBGSStationServicesV5(BaseModel):
    name: Optional[str] = None
    name_lower: Optional[str] = None


class EBGSSystemRefV5(BaseModel):
    system_id: Optional[str] = None
    name: Optional[str] = None
    name_lower: Optional[str] = None


class TickTimesHistoryV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    time: Optional[str] = None
    updated_at: Optional[str] = None


class TickTimesV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    time: Optional[str] = None
    updated_at: Optional[str] = None
    history: Optional[List[TickTimesHistoryV5]] = None


class EBGSFactionHistorySystemV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    faction_name: Optional[str] = None
    faction_name_lower: Optional[str] = None
    faction_id: Optional[str] = None
    state: Optional[str] = None
    influence: Optional[float] = None
    happiness: Optional[str] = None
    active_states: Optional[List[EBGSStateActiveV5]] = None
    pending_states: Optional[List[EBGSStateV5]] = None
    recovering_states: Optional[List[EBGSStateV5]] = None
    conflicts: Optional[List[EBGSConflictFactionV5]] = None
    systems: Optional[List[EBGSSystemRefV5]] = None


class EBGSFactionHistoryV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    system: Optional[str] = None
    system_lower: Optional[str] = None
    system_id: Optional[str] = None
    state: Optional[str] = None
    influence: Optional[float] = None
    happiness: Optional[str] = None
    active_states: Optional[List[EBGSStateActiveV5]] = None
    pending_states: Optional[List[EBGSStateV5]] = None
    recovering_states: Optional[List[EBGSStateV5]] = None
    conflicts: Optional[List[EBGSConflictFactionV5]] = None
    systems: Optional[List[EBGSSystemRefV5]] = None


class EBGSStationHistoryV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    government: Optional[str] = None
    allegiance: Optional[str] = None
    state: Optional[str] = None
    controlling_minor_faction_cased: Optional[str] = None
    controlling_minor_faction: Optional[str] = None
    controlling_minor_faction_id: Optional[str] = None
    services: Optional[List[EBGSStationServicesV5]] = None


class EBGSStationsV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    eddb_id: Optional[int] = None
    name: Optional[str] = None
    name_lower: Optional[str] = None
    name_aliases: Optional[List[EBGSNameAliasV5]] = None
    market_id: Optional[str] = None
    type: Optional[str] = None
    system: Optional[str] = None
    system_lower: Optional[str] = None
    system_id: Optional[str] = None
    updated_at: Optional[str] = None
    government: Optional[str] = None
    economy: Optional[str] = None
    all_economies: Optional[List[EBGSAllEconomiesV5]] = None
    allegiance: Optional[str] = None
    state: Optional[str] = None
    distance_from_star: Optional[int] = None
    controlling_minor_faction_cased: Optional[str] = None
    controlling_minor_faction: Optional[str] = None
    controlling_minor_faction_id: Optional[str] = None
    services: Optional[List[EBGSStationServicesV5]] = None
    history: Optional[List[EBGSStationHistoryV5]] = None


class EBGSStationsPageV5(BaseModel):
    docs: Optional[List[EBGSStationsV5]] = None
    total: Optional[int] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    pages: Optional[int] = None


class EBGSFactionPresenceV5(BaseModel):
    system_name: Optional[str] = None
    system_name_lower: Optional[str] = None
    system_id: Optional[str] = None
    state: Optional[str] = None
    influence: Optional[float] = None
    happiness: Optional[str] = None
    active_states: Optional[List[EBGSStateActiveV5]] = None
    pending_states: Optional[List[EBGSStateV5]] = None
    recovering_states: Optional[List[EBGSStateV5]] = None
    conflicts: Optional[List[EBGSConflictFactionV5]] = None
    system_details: Optional[EBGSSystemsV5] = None
    updated_at: Optional[str] = None

    def getallstates(self):
        active_states = []
        pending_states = []
        recovering_states = []
        for astate in self.active_states:
            active_states.append(astate.state)
        for pstate in self.pending_states:
            pending_states.append(pstate.state)
        for rstate in self.recovering_states:
            recovering_states.append(rstate.state)
        return {'active': active_states, 'pending': pending_states,
                'recovering': recovering_states}


class EBGSFactionRefV5(BaseModel):
    faction_id: Optional[str] = None
    name: Optional[str] = None
    name_lower: Optional[str] = None
    faction_details: Optional[EBGSFactionsV5] = None


class EBGSFactionsV5(BaseModel):
    _id: Optional[str] = None
    __v: Optional[int] = None
    eddb_id: Optional[int] = None
    name: Optional[str] = None
    name_lower: Optional[str] = None
    updated_at: Optional[str] = None
    government: Optional[str] = None
    allegiance: Optional[str] = None
    home_system_name: Optional[str] = None
    is_player_faction: Optional[bool] = None
    faction_presence: Optional[EBGSFactionPresenceV5] = None
    history: Optional[List[EBGSFactionHistoryV5]] = None


class EBGSSystemHistoryV5(BaseModel):
    _id: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    population: Optional[int] = None
    government: Optional[str] = None
    allegiance: Optional[str] = None
    state: Optional[str] = None
    security: Optional[str] = None
    controlling_minor_faction_cased: Optional[str] = None
    controlling_minor_faction: Optional[str] = None
    controlling_minor_faction_id: Optional[str] = None
    factions: Optional[List[EBGSFactionRefV5]] = None
    conflicts: Optional[List[EBGSConflictSystemV5]] = None


class EBGSSystemsV5(BaseModel):
    _id: Optional[str] = None
    id: Optional[str] = None
    __v: Optional[int] = None
    eddb_id: Optional[int] = None
    name: Optional[str] = None
    name_lower: Optional[str] = None
    name_aliases: Optional[List[EBGSNameAliasV5]] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    system_address: Optional[str] = None
    population: Optional[int] = None
    government: Optional[str] = None
    allegiance: Optional[str] = None
    state: Optional[str] = None
    security: Optional[str] = None
    primary_economy: Optional[str] = None
    secondary_economy: Optional[str] = None
    needs_permit: Optional[bool] = None
    reserve_type: Optional[str] = None
    controlling_minor_faction_cased: Optional[str] = None
    controlling_minor_faction: Optional[str] = None
    controlling_minor_faction_id: Optional[str] = None
    factions: Optional[List[EBGSFactionRefV5]] = None
    conflicts: Optional[List[EBGSConflictSystemV5]] = None
    faction_history: Optional[List[EBGSFactionHistorySystemV5]] = None
    history: Optional[List[EBGSSystemHistoryV5]] = None
    updated_at: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.id = data['_id']


class EBGSFactionsPageV5(BaseModel):
    docs: Optional[List[EBGSFactionsV5]] = None
    total: Optional[int] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    pages: Optional[int] = None


class EBGSSystemsPageV5(BaseModel):
    docs: Optional[List[EBGSSystemsV5]] = None
    total: Optional[int] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    pages: Optional[int] = None


EBGSFactionPresenceV5.update_forward_refs()
EBGSFactionRefV5.update_forward_refs()
