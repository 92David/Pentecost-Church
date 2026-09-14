from sqlalchemy import Boolean, Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="member")
    status = Column(String, nullable=False, default="active")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    birthday = Column(String, nullable=True)
    member_number = Column(String, nullable=True)
    join_date = Column(String, nullable=True)
    ministry = Column(String, nullable=True)


class Pastor(Base):
    __tablename__ = "pastors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)


class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    details = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service_day = Column(String, nullable=False)
    service_time = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)


class Sermon(Base):
    __tablename__ = "sermons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    preacher = Column(String, nullable=False)
    sermon_date = Column(String, nullable=False)
    bible_scripture = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default="published")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(String, nullable=False)
    event_time = Column(String, nullable=True)
    location = Column(String, nullable=True)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)


class BibleVerse(Base):
    __tablename__ = "bible_verses"

    id = Column(Integer, primary_key=True, index=True)
    verse_text = Column(Text, nullable=False)
    reference = Column(String, nullable=False)
    theme = Column(String, nullable=True)
    verse_date = Column(String, nullable=True)


class DailyQuote(Base):
    __tablename__ = "daily_quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote_text = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    quote_date = Column(String, nullable=False)
    category = Column(String, nullable=True)
    status = Column(String, nullable=False, default="published")


class PrayerRequest(Base):
    __tablename__ = "prayer_requests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    category = Column(String, nullable=True)
    prayer_message = Column(Text, nullable=False)
    is_private = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="pending")


class Offering(Base):
    __tablename__ = "offerings"

    id = Column(Integer, primary_key=True, index=True)
    offering_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    donor_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="completed")


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publish_date = Column(String, nullable=True)
    status = Column(String, nullable=False, default="published")


class GalleryItem(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    opening_hours = Column(Text, nullable=True)
    sunday_service_times = Column(Text, nullable=True)
    map_url = Column(String, nullable=True)
    message = Column(Text, nullable=True)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
