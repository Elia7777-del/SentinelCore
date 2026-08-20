import os
from uuid import uuid4
from app.db.session import Base, engine, SessionLocal
from app.models import Organization, User
from app.services.security import hash_password

Base.metadata.create_all(bind=engine)

email = os.environ.get("SENTINELCORE_ADMIN_EMAIL")
password = os.environ.get("SENTINELCORE_ADMIN_PASSWORD")
organization = os.environ.get("SENTINELCORE_ORGANIZATION", "Default Organization")

if not email or not password or len(password) < 12:
    raise SystemExit("Set SENTINELCORE_ADMIN_EMAIL and SENTINELCORE_ADMIN_PASSWORD (12+ characters).")

db = SessionLocal()
try:
    org = db.query(Organization).filter(Organization.name == organization).first()
    if not org:
        org = Organization(id=str(uuid4()), name=organization)
        db.add(org)
        db.flush()

    if db.query(User).filter(User.email == email).first():
        raise SystemExit("Admin email already exists.")

    user = User(
        id=str(uuid4()),
        organization_id=org.id,
        email=email,
        password_hash=hash_password(password),
        role="admin",
        mfa_enabled=False,
    )
    db.add(user)
    db.commit()
    print("Admin created.")
finally:
    db.close()
