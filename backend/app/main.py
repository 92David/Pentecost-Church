from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth import create_access_token, get_current_user, get_password_hash, require_staff, verify_password
from .cms import ensure_cms, public_settings, router as admin_router
from .database import get_db
from .models import (
    Announcement,
    BibleVerse,
    Contact,
    DailyQuote,
    Event,
    GalleryItem,
    Member,
    Ministry,
    Notification,
    Offering,
    PrayerRequest,
    Sermon,
    Service,
    User,
)
from .schemas import (
    ContactCreate,
    OfferingCreate,
    PrayerRequestCreate,
    SermonCreate,
    UserCreate,
)


app = FastAPI(title="Pentecost Church Platform", version="1.0.0")
ensure_cms()
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Pentecost Church API is running"}


@app.post("/api/auth/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role="member",
        status="active",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


@app.post("/api/auth/login")
def login(payload: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.username).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "role": user.role, "full_name": user.full_name},
    }


@app.get("/api/users/me")
def get_current_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.user_id == current_user.id).first()
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "status": current_user.status,
        "ministry": member.ministry if member else None,
        "phone": member.phone if member else None,
        "member_number": member.member_number if member else None,
    }


@app.get("/api/site-settings")
def get_site_settings(db: Session = Depends(get_db)):
    return public_settings(db)


@app.get("/api/sermons")
def get_sermons(db: Session = Depends(get_db), category: str | None = Query(default=None), search: str | None = Query(default=None)):
    query = db.query(Sermon).filter(Sermon.status == "published")

    if category:
        query = query.filter(Sermon.category == category)
    if search:
        query = query.filter(Sermon.title.ilike(f"%{search}%"))

    return query.order_by(Sermon.sermon_date.desc()).all()


@app.get("/api/sermons/{sermon_id}")
def get_sermon(sermon_id: int, db: Session = Depends(get_db)):
    sermon = db.query(Sermon).filter(Sermon.id == sermon_id, Sermon.status == "published").first()
    if not sermon:
        raise HTTPException(status_code=404, detail="Sermon not found")
    return sermon


@app.post("/api/sermons")
def create_sermon(payload: SermonCreate, db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    sermon = Sermon(**payload.model_dump())
    db.add(sermon)
    db.commit()
    db.refresh(sermon)
    return sermon


@app.get("/api/events")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.event_date.asc()).all()


@app.get("/api/ministries")
def get_ministries(db: Session = Depends(get_db)):
    return db.query(Ministry).filter(Ministry.status == "active").all()


@app.get("/api/services")
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).order_by(Service.id.asc()).all()


@app.get("/api/verse-of-the-day")
def get_verse_of_the_day(db: Session = Depends(get_db)):
    verse = db.query(BibleVerse).order_by(BibleVerse.verse_date.desc(), BibleVerse.id.desc()).first()
    if not verse:
        raise HTTPException(status_code=404, detail="No verse found")
    return verse


@app.get("/api/bible-verses")
def get_bible_verses(db: Session = Depends(get_db)):
    return db.query(BibleVerse).order_by(BibleVerse.verse_date.desc(), BibleVerse.id.desc()).all()


@app.get("/api/quotes")
def get_quotes(db: Session = Depends(get_db)):
    return db.query(DailyQuote).filter(DailyQuote.status == "published").order_by(DailyQuote.quote_date.desc()).all()


@app.get("/api/gallery")
def get_gallery(db: Session = Depends(get_db)):
    return db.query(GalleryItem).order_by(GalleryItem.id.desc()).all()


@app.post("/api/prayer-requests")
def create_prayer_request(payload: PrayerRequestCreate, db: Session = Depends(get_db)):
    request_item = PrayerRequest(**payload.model_dump())
    db.add(request_item)
    db.commit()
    db.refresh(request_item)
    return {"message": "Prayer request submitted successfully", "request_id": request_item.id}


@app.get("/api/prayer-requests")
def list_prayer_requests(db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    return db.query(PrayerRequest).order_by(PrayerRequest.id.desc()).all()


@app.get("/api/prayer-requests/me")
def list_my_prayer_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(PrayerRequest)
        .filter(PrayerRequest.email == current_user.email)
        .order_by(PrayerRequest.id.desc())
        .all()
    )


@app.post("/api/offerings")
def create_offering(payload: OfferingCreate, db: Session = Depends(get_db)):
    offering = Offering(**payload.model_dump())
    db.add(offering)
    db.commit()
    db.refresh(offering)
    return {"message": "Offering recorded successfully", "offering_id": offering.id}


@app.get("/api/offerings")
def list_offerings(db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    return db.query(Offering).order_by(Offering.id.desc()).all()


@app.get("/api/offerings/me")
def list_my_offerings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Offering).filter(Offering.email == current_user.email).order_by(Offering.id.desc()).all()


@app.post("/api/contacts")
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"subject"})
    subject = payload.subject.strip() if payload.subject else ""
    message = data.get("message") or ""
    if subject:
        data["message"] = f"{subject}: {message}".strip()
    contact = Contact(**data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return {"message": "Contact message saved successfully", "contact_id": contact.id}


@app.get("/api/announcements")
def get_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).filter(Announcement.status == "published").order_by(Announcement.publish_date.desc()).all()


@app.get("/api/contacts")
def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    return db.query(Contact).order_by(Contact.id.desc()).all()


@app.get("/api/notifications")
def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Notification)
        .filter((Notification.user_id == current_user.id) | (Notification.user_id.is_(None)))
        .order_by(Notification.id.desc())
        .all()
    )


@app.get("/api/members")
def list_members(db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    rows = db.query(Member, User).join(User, Member.user_id == User.id).all()
    return [
        {
            "id": member.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "phone": member.phone,
            "ministry": member.ministry,
            "member_number": member.member_number,
        }
        for member, user in rows
    ]
