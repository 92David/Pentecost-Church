import csv
import io
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .auth import require_staff
from .database import Base, engine, get_db
from .models import (
    Announcement,
    BibleVerse,
    DailyQuote,
    Event,
    GalleryItem,
    Ministry,
    Sermon,
    SiteSetting,
    User,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DEFAULT_SETTINGS = {
    "church_name": "Pentecost Church",
    "hero_eyebrow": "Growing in faith together",
    "hero_title": "Encounter God, build community, and serve with purpose.",
    "hero_text": "We are a vibrant church family centered on worship, prayer, discipleship, and reaching people with the love of Jesus Christ.",
    "this_week_title": "Sunday Worship",
    "this_week_times": "9:00 AM • 11:00 AM • 6:30 PM",
    "contact_address": "123 Grace Avenue\nCity, State",
    "contact_phone": "(123) 456-7890",
    "contact_email": "hello@pentecostchurch.org",
    "opening_hours": "Monday - Friday\n9:00 AM - 5:00 PM",
    "sunday_times": "9:00 AM\n11:00 AM\n6:30 PM",
    "footer_address": "123 Grace Avenue • City, State",
    "show_giving": "true",
    "show_contact": "true",
    "show_search": "true",
}

RESOURCES = {
    "sermons": {
        "model": Sermon,
        "fields": [
            "title",
            "preacher",
            "sermon_date",
            "bible_scripture",
            "description",
            "category",
            "status",
            "thumbnail_url",
            "video_url",
            "audio_url",
            "notes",
        ],
        "required": ["title", "preacher", "sermon_date", "bible_scripture", "category"],
        "defaults": {"status": "published"},
        "label": "title",
    },
    "events": {
        "model": Event,
        "fields": ["title", "description", "event_date", "event_time", "location", "category", "image_url"],
        "required": ["title", "event_date"],
        "defaults": {},
        "label": "title",
    },
    "ministries": {
        "model": Ministry,
        "fields": ["name", "tagline", "description", "details", "image_url", "status"],
        "required": ["name"],
        "defaults": {"status": "active"},
        "label": "name",
    },
    "bible-verses": {
        "model": BibleVerse,
        "fields": ["verse_text", "reference", "theme", "verse_date"],
        "required": ["verse_text", "reference"],
        "defaults": {},
        "label": "reference",
    },
    "quotes": {
        "model": DailyQuote,
        "fields": ["quote_text", "author", "quote_date", "category", "status"],
        "required": ["quote_text", "author", "quote_date"],
        "defaults": {"status": "published"},
        "label": "quote_text",
    },
    "gallery": {
        "model": GalleryItem,
        "fields": ["title", "image_url", "description", "category"],
        "required": ["title", "image_url"],
        "defaults": {},
        "label": "title",
    },
    "announcements": {
        "model": Announcement,
        "fields": ["title", "content", "publish_date", "status"],
        "required": ["title", "content"],
        "defaults": {"status": "published"},
        "label": "title",
    },
}

router = APIRouter(prefix="/api/admin", dependencies=[Depends(require_staff)])


def ensure_cms() -> None:
    Base.metadata.create_all(bind=engine)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = next(get_db())
    try:
        seed_default_settings(db)
        for name in RESOURCES:
            write_csv_snapshot(name, db)
        write_settings_csv(db)
    finally:
        db.close()


def seed_default_settings(db: Session) -> None:
    existing = {row.key for row in db.query(SiteSetting).all()}
    for key, value in DEFAULT_SETTINGS.items():
        if key not in existing:
            db.add(SiteSetting(key=key, value=value))
    db.commit()


def public_settings(db: Session) -> dict[str, str]:
    seed_default_settings(db)
    rows = db.query(SiteSetting).all()
    return {row.key: row.value or "" for row in rows}


def get_resource(name: str) -> dict:
    resource = RESOURCES.get(name)
    if not resource:
        raise HTTPException(status_code=404, detail="Unknown resource")
    return resource


def to_dict(item) -> dict:
    return {column.name: getattr(item, column.name) for column in item.__table__.columns}


def clean_payload(resource: dict, payload: dict, partial: bool = False) -> dict:
    data = {}
    for field in resource["fields"]:
        if field in payload:
            value = payload[field]
            data[field] = value.strip() if isinstance(value, str) else value
        elif not partial and field in resource["defaults"]:
            data[field] = resource["defaults"][field]
    if not partial:
        missing = [field for field in resource["required"] if not data.get(field)]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing fields: {', '.join(missing)}")
    return data


def write_csv_snapshot(name: str, db: Session) -> Path:
    resource = get_resource(name)
    rows = db.query(resource["model"]).all()
    path = DATA_DIR / f"{name}.csv"
    fieldnames = ["id", *resource["fields"]]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            item = to_dict(row)
            writer.writerow({key: item.get(key, "") if item.get(key) is not None else "" for key in fieldnames})
    return path


def write_settings_csv(db: Session) -> Path:
    path = DATA_DIR / "site-settings.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"])
        writer.writeheader()
        for key, value in public_settings(db).items():
            writer.writerow({"key": key, "value": value})
    return path


@router.get("/site-settings")
def admin_get_settings(db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    return public_settings(db)


@router.put("/site-settings")
def admin_update_settings(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Settings must be an object")

    for key, value in payload.items():
        row = db.query(SiteSetting).filter(SiteSetting.key == str(key)).first()
        stored = "" if value is None else str(value)
        if row:
            row.value = stored
        else:
            db.add(SiteSetting(key=str(key), value=stored))
    db.commit()
    write_settings_csv(db)
    return public_settings(db)


@router.get("/csv/{resource}")
def export_csv(resource: str, db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    if resource == "site-settings":
        path = write_settings_csv(db)
    else:
        path = write_csv_snapshot(resource, db)
    content = path.read_bytes()
    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{path.name}"'},
    )


@router.post("/csv/{resource}")
async def import_csv(
    resource: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    raw = (await file.read()).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw))

    if resource == "site-settings":
        for row in reader:
            key = (row.get("key") or "").strip()
            if not key:
                continue
            value = row.get("value") or ""
            existing = db.query(SiteSetting).filter(SiteSetting.key == key).first()
            if existing:
                existing.value = value
            else:
                db.add(SiteSetting(key=key, value=value))
        db.commit()
        write_settings_csv(db)
        return public_settings(db)

    spec = get_resource(resource)
    model = spec["model"]
    imported = 0
    for row in reader:
        payload = {field: row.get(field, "") for field in spec["fields"]}
        data = clean_payload(spec, payload)
        item_id = str(row.get("id") or "").strip()
        existing = db.query(model).filter(model.id == int(item_id)).first() if item_id.isdigit() else None
        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
        else:
            db.add(model(**data))
        imported += 1
    db.commit()
    write_csv_snapshot(resource, db)
    return {"message": f"Imported {imported} {resource} records"}


@router.get("/{resource}")
def list_admin_resource(resource: str, db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    spec = get_resource(resource)
    return [to_dict(item) for item in db.query(spec["model"]).order_by(spec["model"].id.desc()).all()]


@router.post("/{resource}")
def create_admin_resource(
    resource: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    spec = get_resource(resource)
    data = clean_payload(spec, payload)
    item = spec["model"](**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    write_csv_snapshot(resource, db)
    return to_dict(item)


@router.put("/{resource}/{item_id}")
def update_admin_resource(
    resource: str,
    item_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    spec = get_resource(resource)
    item = db.query(spec["model"]).filter(spec["model"].id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Record not found")
    data = clean_payload(spec, payload, partial=True)
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    write_csv_snapshot(resource, db)
    return to_dict(item)


@router.delete("/{resource}/{item_id}")
def delete_admin_resource(
    resource: str,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    spec = get_resource(resource)
    item = db.query(spec["model"]).filter(spec["model"].id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(item)
    db.commit()
    write_csv_snapshot(resource, db)
    return {"message": "Deleted"}
