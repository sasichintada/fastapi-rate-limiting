from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from datetime import datetime
import uuid

class APIKeyService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_api_key(self, client_name: str, email: str) -> APIKey:
        api_key = APIKey(
            api_key=str(uuid.uuid4()),
            client_name=client_name,
            email=email
        )
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key
    
    def get_api_key(self, api_key: str) -> APIKey:
        return self.db.query(APIKey).filter(
            APIKey.api_key == api_key,
            APIKey.is_active == True
        ).first()
    
    def validate_api_key(self, api_key: str) -> bool:
        key = self.get_api_key(api_key)
        return key is not None
    
    def update_last_used(self, api_key: str):
        key = self.get_api_key(api_key)
        if key:
            key.last_used_at = datetime.utcnow()
            key.total_requests += 1
            self.db.commit()
    
    def revoke_api_key(self, api_key: str) -> bool:
        key = self.get_api_key(api_key)
        if key:
            key.is_active = False
            self.db.commit()
            return True
        return False
    
    def get_all_keys(self, skip: int = 0, limit: int = 100):
        return self.db.query(APIKey).offset(skip).limit(limit).all()