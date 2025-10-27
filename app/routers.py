from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .database import get_db
from .schemas import DeviceCreate, DeviceOut, DeviceUpdate, BatteryCreate, BatteryOut, BatteryUpdate

router = APIRouter()

# Devices
@router.get('/devices/', response_model=list[DeviceOut])
async def read_devices(db: AsyncSession = Depends(get_db)):
    return await crud.get_devices(db)

@router.post('/devices/', response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create_device(payload: DeviceCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_device(db, payload)

@router.get('/devices/{device_id}', response_model=DeviceOut)
async def get_device(device_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_device(db, device_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Device not found')
    return obj

@router.put('/devices/{device_id}', response_model=DeviceOut)
async def update_device(device_id: int, payload: DeviceUpdate, db: AsyncSession = Depends(get_db)):
    values = {k: v for k, v in payload.dict().items() if v is not None}
    obj = await crud.get_device(db, device_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Device not found')
    return await crud.update_device(db, device_id, values)

@router.delete('/devices/{device_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_device(db, device_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Device not found')
    await crud.delete_device(db, device_id)
    return None

# Batteries
@router.get('/batteries/', response_model=list[BatteryOut])
async def read_batteries(db: AsyncSession = Depends(get_db)):
    return await crud.get_batteries(db)

@router.post('/batteries/', response_model=BatteryOut, status_code=status.HTTP_201_CREATED)
async def create_battery(payload: BatteryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_battery(db, payload)

@router.get('/batteries/{battery_id}', response_model=BatteryOut)
async def get_battery(battery_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_battery(db, battery_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Battery not found')
    return obj

@router.put('/batteries/{battery_id}', response_model=BatteryOut)
async def update_battery(battery_id: int, payload: BatteryUpdate, db: AsyncSession = Depends(get_db)):
    values = {k: v for k, v in payload.dict().items() if v is not None}
    obj = await crud.get_battery(db, battery_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Battery not found')
    return await crud.update_battery(db, battery_id, values)

@router.delete('/batteries/{battery_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_battery(battery_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud.get_battery(db, battery_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Battery not found')
    await crud.delete_battery(db, battery_id)
    return None

# Association endpoints
@router.post('/devices/{device_id}/attach/{battery_id}', response_model=BatteryOut)
async def attach_battery(device_id: int, battery_id: int, db: AsyncSession = Depends(get_db)):
    device = await crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    battery = await crud.get_battery(db, battery_id)
    if not battery:
        raise HTTPException(status_code=404, detail='Battery not found')
    try:
        updated = await crud.attach_battery_to_device(db, device, battery)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/devices/{device_id}/detach/{battery_id}', response_model=BatteryOut)
async def detach_battery(device_id: int, battery_id: int, db: AsyncSession = Depends(get_db)):
    device = await crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    battery = await crud.get_battery(db, battery_id)
    if not battery:
        raise HTTPException(status_code=404, detail='Battery not found')
    if battery.device_id != device.id:
        raise HTTPException(status_code=400, detail='Battery not attached to this device')
    updated = await crud.detach_battery(db, battery)
    return updated
