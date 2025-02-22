import httpx
import json
from fastapi import HTTPException
from app.config import settings


class DirectusService:
    def __init__(self):
        self.api_token = settings.DIRECTUS_API_TOKEN
        self.base_url = settings.DIRECTUS_API_URL
        self.email = settings.DIRECTUS_ADMIN_EMAIL
        self.password = settings.DIRECTUS_ADMIN_PASSWORD
        
    async def _get_access_token(self):
        """
        Obtain a new access token from Directus
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={
                        "email": self.email,
                        "password": self.password
                    }
                )
                
                print("Token Generation Response Status:", response.status_code)
                print("Token Generation Response Body:", response.text)
                
                response.raise_for_status()
                token_data = response.json()
                
                # Update the API token
                self.api_token = token_data['data']['access_token']
                return self.api_token
        except Exception as e:
            print(f"Token Generation Error: {e}")
            raise HTTPException(
                status_code=401, 
                detail="Could not generate authentication token"
            )

    async def create_booking(self, booking_data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/items/bookings",
                    headers={
                        "Authorization": f"Bearer {self.api_token}",
                        "Content-Type": "application/json"
                    },
                    json=booking_data
                )
                
                # Print full response for debugging
                print("Directus Create Booking Response Status:", response.status_code)
                print("Directus Create Booking Response Body:", response.text)
                
                # If unauthorized, try to refresh token and retry
                if response.status_code == 401:
                    await self._get_access_token()
                    # Retry with new token
                    response = await client.post(
                        f"{self.base_url}/items/bookings",
                        headers={
                            "Authorization": f"Bearer {self.api_token}",
                            "Content-Type": "application/json"
                        },
                        json=booking_data
                    )
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP Error in Create Booking: {http_err}")
            print(f"Response Body: {http_err.response.text}")
            raise HTTPException(
                status_code=http_err.response.status_code, 
                detail=f"Booking creation failed: {http_err.response.text}"
            )
        except Exception as e:
            print(f"Unexpected error in Create Booking: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Unexpected error: {str(e)}"
            )

    async def get_booking(self, booking_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/items/bookings/{booking_id}",
                    headers={
                        "Authorization": f"Bearer {self.api_token}",
                        "Content-Type": "application/json"
                    }
                )
                
                print("Get Booking Response Status:", response.status_code)
                print("Get Booking Response Headers:", response.headers)
                
                # If unauthorized, try to refresh token and retry
                if response.status_code == 401:
                    await self._get_access_token()
                    # Retry with new token
                    response = await client.get(
                        f"{self.base_url}/items/bookings/{booking_id}",
                        headers={
                            "Authorization": f"Bearer {self.api_token}",
                            "Content-Type": "application/json"
                        }
                    )
                
                # Try to parse the response and print details
                try:
                    response_json = response.json()
                    print("Full Response JSON:", json.dumps(response_json, indent=2))
                except Exception as e:
                    print(f"Error parsing JSON: {e}")
                    print("Response Text:", response.text)
                
                response.raise_for_status()
                return response_json
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP Error in Get Booking: {http_err}")
            print(f"Response Body: {http_err.response.text}")
            raise HTTPException(
                status_code=http_err.response.status_code, 
                detail=f"Booking retrieval failed: {http_err.response.text}"
            )
        except Exception as e:
            print(f"Unexpected error in Get Booking: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Unexpected error: {str(e)}"
            )