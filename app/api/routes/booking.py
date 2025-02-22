from fastapi import APIRouter, HTTPException, Depends
from app.api.models.booking import BookingRequest, BookingResponse, BookingDetails
from app.services.odoo.odoo import OdooService
from app.services.calcom.calcom import CalComService
from app.services.directus.directus import DirectusService
from app.core.security import verify_api_key
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/")
async def create_booking(
    booking_data: BookingRequest = Body(...),
    directus_service: DirectusService = Depends(),
    odoo_service: OdooService = Depends(),
    #calcom_service: CalComService = Depends()
):
    try:
        print("Booking Data:", booking_data.model_dump())

        order_result = await odoo_service.create_order(
            customer_id=booking_data.customer_id,
            service_id=booking_data.service_id
        )
        odoo_order_id = order_result.get('order_id')
        odoo_invoice_id = order_result.get('invoice_id')

        #cal_booking = await calcom_service.schedule_appointment(
        #    date=booking_data.date,
        #    time=booking_data.time,
        #    customer_id=booking_data.customer_id,
        #    service_id=int(booking_data.service_id)
        #)
        #cal_booking_id = cal_booking.get('id', '')
        
        # Prepare booking record for Directus
        directus_booking_data = {
            "customer_id": booking_data.customer_id,
            "service_id": booking_data.service_id,
            "date": booking_data.date,
            "time": booking_data.time,
            "order_id": odoo_order_id,
            "invoice_id": odoo_invoice_id,
            "cal_booking_id": "1",
            "status": booking_data.status or "confirmed",
            "additional_info": booking_data.additional_info
        }
        
        
        # Store booking in Directus
        booking_record = await directus_service.create_booking(directus_booking_data)
        print("booking_record")
        print(booking_record)
        return BookingResponse(
            message="Booking processed successfully",
            order_id=booking_record['data'].get('order_id', 0),
            invoice_id=booking_record['data'].get('invoice_id', 0),
            cal_booking_id=booking_record['data'].get('cal_booking_id', ""),
            status=booking_record['data'].get('status', "confirmed")
        )
        
    except Exception as e:
        print(f"Error in create_booking: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process booking: {str(e)}"
        )


@router.get("/{booking_id}", response_model=BookingDetails)
async def get_booking(
    booking_id: str,
    directus_service: DirectusService = Depends()
):
    try:
        booking_response = await directus_service.get_booking(booking_id)
        print("Full booking response:", booking_response)
        
        # Directus typically returns data in a 'data' key
        booking = booking_response.get('data', booking_response)
        print("Processed booking:", booking)

        # Prepare a dictionary with all possible fields
        booking_data = {
            'id': booking.get('id'),
            'customer_id': booking.get('customer_id', 0),
            'service_id': booking.get('service_id', 0),
            'date': booking.get('date', ''),
            'time': booking.get('time', ''),
            'order_id': str(booking.get('order_id', '')),
            'invoice_id': str(booking.get('invoice_id', '')),
            'cal_booking_id': booking.get('cal_booking_id', None),
            'status': booking.get('status', 'pending'),
            'additional_info': booking.get('additional_info')
        }

        # Create the BookingDetails instance
        booking_details = BookingDetails(**booking_data)

        return booking_details
    except Exception as e:
        print(f"Error in get_booking: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch booking: {str(e)}"
        )