from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse
from app.schemas.borrow import BorrowResponse

router = APIRouter(
    prefix="/members",
    tags=["Members"]
)

# Get all members
@router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

# Get member by ID
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# Get borrowing history of a member
@router.get("/{member_id}/borrows", response_model=list[BorrowResponse])
def get_member_borrow_history(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member.borrows

# Create member
@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    if db.query(Member).filter(Member.email == member.email).first():
        raise HTTPException(status_code=400, detail="Member with this email already exists")

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# Update member
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    update_data = member_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)
    return member