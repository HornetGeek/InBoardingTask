import httpx
from app.config import settings
from fastapi import HTTPException
from typing import Dict, Any
import json

class CalComServiceError(Exception):
    """Custom exception for CalComService errors"""
    def __init__(self, message: str, status_code: int = None, response_data: Dict[str, Any] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)

class CalComService:
    def __init__(self):
        self.api_key = settings.CALCOM_API_KEY
        self.base_url = settings.CALCOM_API_URL
        
    async def schedule_appointment(self, date, time, customer_id: int, service_id: int):
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/v2/bookings"
                
                # Clean up the date string
                date_str = str(date).split('T')[0].strip()
                time_str = str(time).strip()

                print(f"Cleaned Date: {date_str}, Time: {time_str}")
                
                # Create the datetime objects
                from datetime import datetime, timedelta
                start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                
                # Wrap the entire payload in a data object
                payload = {
                    "start": "2024-08-13T09:00:00Z",
                    "lengthInMinutes": 30,
                    "eventTypeId": 123,
                    "attendee": {
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "timeZone": "America/New_York",
                        "phoneNumber": "+919876543210",
                        "language": "it"
                    },
                    "guests": ["guest1@example.com", "guest2@example.com"],
                    "meetingUrl": "https://example.com/meeting",
                    "location": "https://example.com/meeting",
                    "metadata": {"key": "value"},
                    "bookingFieldsResponses": {"customField": "customValue"}
                }
                
                print("Cal.com API Request URL:", url)
                print("Cal.com API Request Payload:", json.dumps(payload, indent=2))
                
                response = await client.post(
                    url,
                    json=payload,
                    timeout=30.0,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}",
                        "cal-api-version": "2.0"
                    }
                )
                
                print("Cal.com API Response Status Code:", response.status_code)
                print("Cal.com API Response Headers:", dict(response.headers))
                print("Cal.com API Raw Response:", response.text)
                
                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                        error_message = error_data.get('error', {}).get('message', 'Unknown error')
                        error_details = error_data.get('error', {}).get('details', {})
                        raise CalComServiceError(
                            message=f"Cal.com API error: {error_message}. Details: {error_details}",
                            status_code=response.status_code,
                            response_data=error_data
                        )
                    except json.JSONDecodeError:
                        raise CalComServiceError(
                            message=f"Cal.com API error: {response.text}",
                            status_code=response.status_code,
                            response_data={"raw_response": response.text}
                        )
                
                return response.json()
                    
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            print(f"Error Type: {type(e)}")
            if hasattr(e, '__traceback__'):
                import traceback
                print("Traceback:", traceback.format_exc())
            raise CalComServiceError(
                message=f"Unexpected error scheduling appointment: {str(e)}",
                status_code=500
            )





