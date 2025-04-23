from datetime import datetime, date
from random import randint
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item as PyInvoiceItem, Transaction
from pyinvoice.templates import SimpleInvoice as SI


doc = SI("test_invoice2.pdf")
now = datetime.now()
doc.invoice_info = InvoiceInfo(f"INV-{randint(100, 999)}", now.strftime("%d/%m/%Y %I:%M%p"))
doc.service_provider_info = ServiceProviderInfo("AquaLab Ozono y Salud SAS", "Calle 1", "Barranquilla", country="Colombia",
                                            vat_tax_number="123456")
doc.client_info = ClientInfo(name="Yhoxin Rossell", email= "yhoxrossell508@gmail.com", client_id=f"CLI-{randint(100, 999)}", nit="123456")
doc.add_item(PyInvoiceItem("Filtro de agua", "Servicio de instalación de filtro de agua", 2, 140000,))

doc.set_bottom_tip("¡Gracias por su compra!")

doc.finish()