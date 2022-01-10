from pydantic import BaseModel, ValidationError, validator, root_validator, parse_obj_as
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import json
import orjson
import dpath.util

class ServicesEnum(Enum):
    calc = 'calculator'
    bpm = 'bpm'

class Client(BaseModel):
    id: str

class Manager(BaseModel):
    id: str
    name: str

class Branch(BaseModel):
    id: str
    name: str

class Contract(BaseModel):
    id: str
    type: str
    branch: Branch
    number: str
    language: str
    date_expiration: datetime


class Additional(BaseModel):
    currency: str
    client_type: str
    wagon_owner: str
    linked_cargo: Optional[str]
    user_type_id: List[int]
    wagons_group: bool
    wagons_linked: bool
    oversize_index: Optional[str]
    sort_routes_by: str
    complex_service: bool
    conductor_count: Optional[int]
    container_owner: str
    empty_equipment: bool
    wagons_in_route: bool
    sales_channel_id: int
    shipment_type_id: int
    household_exceeds: Optional[bool]
    shipment_detail_id: int
    military_form2_rail: bool
    military_form2_water: bool
    wagons_count_in_group: List[int]
    complete_shipment_wagon: bool
    military_form2_terminal: bool
    equipment_types_together: bool
    included_in_container_train: bool

class LocationDetails(BaseModel):
    catalog_id: List[str]
    country_id: str


class Location(BaseModel):
    to: LocationDetails
    from_: LocationDetails

    class Config:
        fields = {
            'from_': 'from'
        }


class Wagons(BaseModel):
    type: str
    count: int

class Containers(BaseModel):
    type: str
    count: int
    weight_brutto: int

class DateStart(BaseModel):
    min: datetime

class Items(BaseModel):
    gng_id: str
    weight: int
    declared: Optional[int]
    etsng_id: str

class Period(BaseModel):
    priority: str
    date_start: DateStart


class Data(BaseModel):
    items: List[Items]
    period: Period
    wagons: Optional[List[Wagons]]
    location: Location
    additional: Additional
    containers: Optional[List[Containers]]
    itinerary_id: Optional[str]
    special_rates: Optional[str]
    items_total_weight: int
    items_declared_value: Optional[int]

    @root_validator
    def print(cls, values):
        if not values.get('wagons') and not values.get('containers'):
            raise ValueError('Wagons or Conteiners must be filled')
        return values

class Params(BaseModel):
    data: Data
    client: Client
    manager: Manager
    contract: Contract

class Request(BaseModel):
    action: str
    object: str
    priority: int
    system_to: str
    message_id: str
    api_version: str
    params: Params
    system_from: ServicesEnum
    reference_id: str
    datetime_created: datetime



#request_file = open('request.json').read()
try:
    
    request = Request.parse_file('request.json')
except ValidationError as err:
    #print(f"{err.__class__} -> {err}")
    print(err)
except json.decoder.JSONDecodeError as err:
    print(err)


