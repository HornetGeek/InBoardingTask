from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Odoo Settings
    ODOO_URL: str 
    ODOO_DB: str
    ODOO_USERNAME: str 
    ODOO_PASSWORD: str 
    
    # Cal.com Settings
    CALCOM_API_KEY: str 
    CALCOM_API_URL: str
    
    # Directus Settings
    DIRECTUS_API_TOKEN: str 
    DIRECTUS_API_URL: str 
    DIRECTUS_ADMIN_EMAIL: str
    DIRECTUS_ADMIN_PASSWORD : str
    # API Settings
    API_KEY: str = "your-api-key"  # Default value
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()



