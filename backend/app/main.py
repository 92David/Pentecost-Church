from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth import create_access_token, get_current_user, get_password_hash, verify_password
from .database import get_db
from .models import (
    Announcement,
    BibleVerse,
    Contact,
    DailyQuote,
    Event,
    GalleryItem,
    Ministry,
    Offering,
    PrayerRequest,
    Sermon,
    User,
)
from .schemas import (
    ContactCreate,
    OfferingCreate,
    PrayerRequestCreate,
    SermonCreate,
    UserCreate,
    UserLogin,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Pentecost Church Platform", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
        role=payload.role,
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
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "role": user.role}}


@app.get("/api/users/me")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "status": current_user.status,
    }


@app.get("/api/sermons")
def get_sermons(db: Session = Depends(get_db), category: str | None = Query(default=None), search: str | None = Query(default=None)):
    query = db.query(Sermon).filter(Sermon.status == "published")

    if category:
        query = query.filter(Sermon.category == category)
    if search:
        query = query.filter(Sermon.title.ilike(f"%{search}%"))

    items = query.order_by(Sermon.sermon_date.desc()).all()
    return items


@app.get("/api/sermons/{sermon_id}")
def get_sermon(sermon_id: int, db: Session = Depends(get_db)):
    sermon = db.query(Sermon).filter(Sermon.id == sermon_id).first()
    if not sermon:
        raise HTTPException(status_code=404, detail="Sermon not found")
    return sermon


@app.post("/api/sermons")
def create_sermon(payload: SermonCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in {"admin", "pastor"}:
        raise HTTPException(status_code=403, detail="Not authorized")

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


@app.get("/api/verse-of-the-day")
def get_verse_of_the_day(db: Session = Depends(get_db)):
    verse = db.query(BibleVerse).order_by(BibleVerse.id.desc()).first()
    if not verse:
        raise HTTPException(status_code=404, detail="No verse found")
    return verse


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


@app.post("/api/offerings")
def create_offering(payload: OfferingCreate, db: Session = Depends(get_db)):
    offering = Offering(**payload.model_dump())
    db.add(offering)
    db.commit()
    db.refresh(offering)
    return {"message": "Offering recorded successfully", "offering_id": offering.id}


@app.post("/api/contacts")
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return {"message": "Contact message saved successfully", "contact_id": contact.id}


@app.get("/api/announcements")
def get_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).filter(Announcement.status == "published").order_by(Announcement.publish_date.desc()).all()


@app.get("/api/contacts")
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).order_by(Contact.id.desc()).all()


@app.get("/api/notifications")
def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Announcement).all()
