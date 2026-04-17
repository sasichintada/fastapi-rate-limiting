from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.usage import UsageRecord
from datetime import datetime, timedelta

class UsageService:
    def __init__(self, db: Session):
        self.db = db
    
    def log_request(self, api_key: str, endpoint: str, method: str, 
                   status_code: int, ip_address: str = None):
        usage = UsageRecord(
            api_key=api_key,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            ip_address=ip_address
        )
        self.db.add(usage)
        self.db.commit()
    
    def get_usage_stats(self, api_key: str, hours: int = 24):
        since = datetime.utcnow() - timedelta(hours=hours)
        
        stats = self.db.query(
            UsageRecord.endpoint,
            func.count(UsageRecord.id).label('request_count')
        ).filter(
            UsageRecord.api_key == api_key,
            UsageRecord.created_at >= since
        ).group_by(UsageRecord.endpoint).all()
        
        total_requests = self.db.query(func.count(UsageRecord.id)).filter(
            UsageRecord.api_key == api_key,
            UsageRecord.created_at >= since
        ).scalar()
        
        return {
            "total_requests": total_requests or 0,
            "endpoint_breakdown": [
                {"endpoint": stat[0], "count": stat[1]} for stat in stats
            ]
        }