from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
import os
import random

os.environ["INVOICE_LANG"] = "es"

def test_invoice_creation():
    client = Client("Juan Pérez", "Avenida Los Médanos", "Coro", "4101", "0412-6435277", "Juanp@gmail.com", "Banco Mercantil")
    provider = Provider("RossTech Solutions", "12345678-9", "Coro", "4101", "0412-1234567", "yhoxrossell508@gmail.com", "Provincial", "010892873881683927", "0108")
    creator = Creator("Yhoxin Rossell", "src/assets/pictures/aqualabLogo.jpg")

    invoice = Invoice(client, provider, creator)
    invoice.add_item(Item(20, 400, "Sistema de facturas", 1, 15))
    invoice.title = "Factura de venta"
    #invoice.custom_fields["Orden de Compra"] = "OC-12345"
    #invoice.custom_fields["Referencia"] = "Proyecto Aqualab"
    #invoice.date = "2023-10-01"
    invoice.currency = "COP"
    invoice.number = str(f"INV-{random.randint(100, 999)}")
    #invoice.lang = "es"
    invoice.currency_locale = "es_CO.UTF-8"


    pdf = SimpleInvoice(invoice)
    
    try:
        pdf.gen("test_invoice.pdf", generate_qr_code=True)
        print("Invoice generated successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

test_invoice_creation()
