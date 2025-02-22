from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Odoo Settings
    ODOO_URL: str = 'http://localhost:8069'
    ODOO_DB: str = 'booking'
    ODOO_USERNAME: str = 'mmoataz03@gmail.com'
    ODOO_PASSWORD: str = 'mwmx-jv53-4bnn'
    
    # Cal.com Settings
    CALCOM_API_KEY: str = 'cal_live_6a1ea678e2d69014c13b2c4596b921ac'
    CALCOM_API_URL: str = 'https://api.cal.com/v1 '
    
    # Directus Settings
    DIRECTUS_API_TOKEN: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImUxNmNmN2U4LWIxM2YtNGE2Yi05ZDEwLWI4OWZiMzNkODhhOCIsInJvbGUiOiI3YmQwOTdmYy0wNjcwLTQ3OWItYTljYi1mY2I3MWY5ZTExM2IiLCJhcHBfYWNjZXNzIjp0cnVlLCJhZG1pbl9hY2Nlc3MiOnRydWUsInNlc3Npb24iOiJFT3NjYzUzY01lZ2lFZUlHa2pqU2s5ZmF3S0hVbGlubXNMV0pKYnVGOGV6VGRMenJ2M2ZGNms3alJyYU5lbjg3IiwiaWF0IjoxNzQwMTY2ODI1LCJleHAiOjE3NDAyNTMyMjUsImlzcyI6ImRpcmVjdHVzIn0.ekGaXdNtao44B9OUQQ0HQjm3yu_F8XZ9l9BF5wAezcs'
    DIRECTUS_API_URL: str = 'http://localhost:8055'
    DIRECTUS_ADMIN_EMAIL: str
    DIRECTUS_ADMIN_PASSWORD : str
    # API Settings
    API_KEY: str = "your-api-key"  # Default value
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()



