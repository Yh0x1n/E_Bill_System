from InvoiceGenerator.api import Invoice, Item as InvoiceItem, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from datetime import datetime, date
from random import randint
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item as PyInvoiceItem, Transaction
from pyinvoice.templates import SimpleInvoice as SI

def generate_invoice():
    # Create a client
    client = Client('John Doe', '123 Main St', 'New York')
    provider = Provider('Jane Smith', '456 Elm St', 'Los Angeles')
    creator = Creator('Marco Lotuffo', "src/assets/pictures/aqualabLogo.jpg")

    invoice = Invoice(client, provider, creator)
    invoice.currency = "COP"
    invoice.currency_locale = 'es_CO.UTF-8'
    #invoice.date = datetime.now()
    invoice.number = f'INV-{randint(100, 999)}'
    invoice.add_item(InvoiceItem(count = 3, price=300000, description="Instalación de filtro de agua", tax = 21))

    pdf_doc = SimpleInvoice(invoice)
    pdf_doc.gen('invoice.pdf')

generate_invoice()

doc = SI("test_invoice2.pdf")

doc.invoice_info = InvoiceInfo(f"INV-{randint(100, 999)}", datetime.now())
doc.service_provider_info = ServiceProviderInfo("AquaLab Ozono y Salud SAS", "Calle 1", "Barranquilla", country="Colombia",
                                            vat_tax_number="123456")
doc.client_info = ClientInfo(name="Yhoxin Rossell", email= "yhoxrossell508@gmail.com", client_id=f"CLI-{randint(100, 999)}")
doc.add_item(PyInvoiceItem("Filtro de agua", "Servicio de instalación de filtro de agua", 2, 140000,))

doc.set_bottom_tip("¡Gracias por su compra!")

doc.finish()