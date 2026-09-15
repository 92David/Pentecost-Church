from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Optional[str] = "member"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class MemberCreate(BaseModel):
    user_id: int
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[str] = None
    member_number: Optional[str] = None
    join_date: Optional[str] = None
    ministry: Optional[str] = None


class SermonCreate(BaseModel):
    title: str
    preacher: str
    sermon_date: str
    bible_scripture: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    notes: Optional[str] = None
    category: str
    thumbnail_url: Optional[str] = None


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: str
    event_time: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None


class PrayerRequestCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    prayer_message: str
    is_private: bool = False


class OfferingCreate(BaseModel):
    offering_type: str
    amount: float
    donor_name: Optional[str] = None
    email: Optional[EmailStr] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None


class ContactCreate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    opening_hours: Optional[str] = None
    sunday_service_times: Optional[str] = None
    map_url: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
