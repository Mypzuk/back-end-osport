from pydantic import BaseModel

class WhitelistIn(BaseModel):
    competition_id: str
    email: str 
    
class CheckWhitelist(BaseModel):
    user_id: str
    competition_id: str