from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sqla_update, delete as sqla_delete
from .models import Device, Battery
from .schemas import DeviceCreate, BatteryCreate

async def get_devices(db: AsyncSession) -> List[Device]:
    q = select(Device)
    res = await db.execute(q)
    return res.scalars().all()

async def get_device(db: AsyncSession, device_id: int) -> Optional[Device]:
    q = select(Device).where(Device.id == device_id)
    res = await db.execute(q)
    return res.scalars().first()

async def create_device(db: AsyncSession, payload: DeviceCreate) -> Device:
    device = Device(**payload.dict())
    db.add(device)
    await db.commit()
    await db.refresh(device)
    return device

async def update_device(db: AsyncSession, device_id: int, values: dict) -> Optional[Device]:
    q = sqla_update(Device).where(Device.id == device_id).values(**values).execution_options(synchronize_session='fetch')
    await db.execute(q)
    await db.commit()
    return await get_device(db, device_id)

async def delete_device(db: AsyncSession, device_id: int) -> bool:
    q = sqla_delete(Device).where(Device.id == device_id)
    await db.execute(q)
    await db.commit()
    return True

# Batteries
async def get_batteries(db: AsyncSession) -> List[Battery]:
    q = select(Battery)
    res = await db.execute(q)
    return res.scalars().all()

async def get_battery(db: AsyncSession, battery_id: int) -> Optional[Battery]:
    q = select(Battery).where(Battery.id == battery_id)
    res = await db.execute(q)
    return res.scalars().first()

async def create_battery(db: AsyncSession, payload: BatteryCreate) -> Battery:
    battery = Battery(**payload.dict())
    db.add(battery)
    await db.commit()
    await db.refresh(battery)
    return battery

async def update_battery(db: AsyncSession, battery_id: int, values: dict) -> Optional[Battery]:
    q = sqla_update(Battery).where(Battery.id == battery_id).values(**values).execution_options(synchronize_session='fetch')
    await db.execute(q)
    await db.commit()
    return await get_battery(db, battery_id)

async def delete_battery(db: AsyncSession, battery_id: int) -> bool:
    q = sqla_delete(Battery).where(Battery.id == battery_id)
    await db.execute(q)
    await db.commit()
    return True

# Association helpers
async def attach_battery_to_device(db: AsyncSession, device: Device, battery: Battery) -> Battery:
    if battery.device_id is not None:
        raise ValueError('battery is already attached to a device')
    if len(device.batteries) >= 5:
        raise ValueError('device already has 5 batteries')
    battery.device_id = device.id
    db.add(battery)
    await db.commit()
    await db.refresh(battery)
    return battery

async def detach_battery(db: AsyncSession, battery: Battery) -> Battery:
    battery.device_id = None
    db.add(battery)
    await db.commit()
    await db.refresh(battery)
    return battery
