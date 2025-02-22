import xmlrpc.client
from app.config import settings
from fastapi import HTTPException



class OdooService:
    def __init__(self):
        self.url = settings.ODOO_URL
        self.db = settings.ODOO_DB
        self.username = settings.ODOO_USERNAME
        self.password = settings.ODOO_PASSWORD
        
        # Print connection details for debugging
        print("Odoo Connection Details:")
        print(f"URL: {self.url}")
        print(f"Database: {self.db}")
        print(f"Username: {self.username}")
        
        # Ensure URL is correct
        if not self.url.startswith(('http://', 'https://')):
            self.url = f'http://{self.url}'
        
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        except Exception as e:
            print(f"Error establishing Odoo connection: {e}")
            raise
        
    async def create_order(self, customer_id: int, service_id: int):
        try:
            print("Starting order creation process")
            
            # Authenticate and get user ID
            try:
                uid = self.common.authenticate(self.db, self.username, self.password, {})
                print(f"Authenticated User ID: {uid}")
                
                if not uid:
                    raise ValueError("Authentication failed. Invalid credentials.")
            except Exception as auth_error:
                print(f"Authentication Error: {auth_error}")
                raise HTTPException(
                    status_code=401, 
                    detail=f"Odoo Authentication Failed: {str(auth_error)}"
                )
            
            # Validate customer and service
            print(f"Attempting to create order with:")
            print(f"Customer ID: {customer_id}")
            print(f"Service ID: {service_id}")
            
            # Detailed error handling for order creation
            try:
                order_id = self.models.execute_kw(
                    self.db, uid, self.password,
                    'sale.order', 'create',
                    [{
                        'partner_id': customer_id,
                        'order_line': [(0, 0, {
                            'product_id': service_id,
                            'product_uom_qty': 1
                        })]
                    }]
                )
                print(f"Order created successfully. Order ID: {order_id}")
                
                # Create invoice
                invoice_id = self.models.execute_kw(
                    self.db, uid, self.password,
                    'account.move', 'create',
                    [{
                        'partner_id': customer_id,
                        'move_type': 'out_invoice',
                        'invoice_origin': f'SO{order_id}'
                    }]
                )
                print(f"Invoice created successfully. Invoice ID: {invoice_id}")
                
                return {"order_id": order_id, "invoice_id": invoice_id}
            
            except xmlrpc.client.Fault as fault:
                print(f"Odoo XML-RPC Fault: {fault.faultCode} - {fault.faultString}")
                raise HTTPException(
                    status_code=403, 
                    detail=f"Odoo Access Denied: {fault.faultString}"
                )
            except Exception as create_error:
                print(f"Order/Invoice Creation Error: {create_error}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to create order/invoice: {str(create_error)}"
                )
        
        except Exception as e:
            print(f"Unexpected error in create_order: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Unexpected Odoo error: {str(e)}"
            )