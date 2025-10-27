from pydantic import BaseModel, conint, confloat
from typing import Optional, List

class BatteryBase(BaseModel):
    name: str
    nominal_voltage: confloat(gt=0)
    remaining_capacity: confloat(ge=0)
    service_life: conint(ge=0)
    device_id: Optional[int] = None

class BatteryCreate(BatteryBase):
    pass

class BatteryUpdate(BaseModel):
    name: Optional[str]
    nominal_voltage: Optional[confloat(gt=0)]
    remaining_capacity: Optional[confloat(ge=0)]
    service_life: Optional[conint(ge=0)]
    device_id: Optional[int]

class BatteryOut(BatteryBase):
    id: int
    device_id: Optional[int]
    class Config:
        orm_mode = True

class DeviceBase(BaseModel):
    name: str
    firmware_version: str
    is_on: bool = True

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    firmware_version: Optional[str]
    is_on: Optional[bool]

class DeviceOut(DeviceBase):
    id: int
    batteries: List[BatteryOut] = []
    class Config:
        orm_mode = True
