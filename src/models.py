import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    username: str
    email: EmailStr
    phoneNumber: str
    address: str

class UserUpdate(BaseModel):
    id: str = Field(alias="_id")
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    phoneNumber: Optional[str]
    address: Optional[str]

class UserResponse2(BaseModel):
    name: str
    email: EmailStr
    phoneNumber: str
    address: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr

class Driver(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    email: EmailStr
    phoneNumber: str
    licence_plate: str
    car_model: str
    coordenates: str
    answer1: str
    answer2: str
    answer3: str

class DriverUpdate(BaseModel):
    id: str = Field(alias="_id")
    name: Optional[str]
    email: Optional[EmailStr]
    phoneNumber: Optional[str]
    licence_plate: Optional[str]
    car_model: Optional[str]
    coordenates: Optional[str]
    answer1: Optional[str]
    answer2: Optional[str]
    answer3: Optional[str]

class DriverResponse(BaseModel):
    id: str
    name: str
    licence_plate: str
    car_model: str
    coordenates: str

class DriverResponse2(BaseModel):
    id: str
    answer1: str
    answer2: str
    answer3: str

class DriverResponse3(BaseModel):
    name: str
    email: str
    phoneNumber: str
        
class Trip(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    begining: str
    destination: str
    date: str
    username: str
    driverId: str

class TripUpdate(BaseModel):
    id: str = Field(alias="_id")
    begining: Optional[str]
    destination: Optional[str]
    date: Optional[str]                         #date is string
    username: Optional[str]
    driverId: Optional[str]

class Payment(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    price: float
    date: str
    travelId: str
    username: str

class PaymentUpdate(BaseModel):
    id: str = Field(alias="_id")
    price: Optional[str]
    destination: Optional[str]
    date: Optional[str]                         #date is string
    travelId: Optional[str]
    username: Optional[str]
