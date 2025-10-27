from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, nullable=False)
    firmware_version = Column(String(64), nullable=False)
    is_on = Column(Boolean, nullable=False, default=True)

    batteries = relationship('Battery', back_populates='device', lazy="selectin")

class Battery(Base):
    __tablename__ = 'batteries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    nominal_voltage = Column(Float, nullable=False)
    remaining_capacity = Column(Float, nullable=False)  # e.g. % или Ah
    service_life = Column(Integer, nullable=False)

    device_id = Column(Integer, ForeignKey('devices.id', ondelete='SET NULL'), nullable=True, default=None)
    device = relationship('Device', back_populates='batteries')

