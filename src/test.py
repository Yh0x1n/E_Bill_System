from datetime import datetime, date
from invoice_lib.templates import SimpleInvoice
from invoice_lib.models import ServiceProviderInfo, ClientInfo, InvoiceInfo, Item

doc = SimpleInvoice('test_invoice.pdf')

doc.invoice_info = InvoiceInfo(invoice_id='1234567890', invoice_datetime=datetime.now(), due_datetime=datetime.now())

doc.service_provider_info = ServiceProviderInfo(name='John Doe', street='123 Main St', city='Anytown',
                                                state='CA', vat_tax_number='123456789', email="JohnDoe@gmail.com",
                                                phone = "123-456-7890")

doc.client_info = ClientInfo(name='Jane Smith', street='456 Elm St', city='Othertown', state='NY',
                             email="JaneSmith@gmail.com", client_id="CLI-123", vat_tax_number="987654321",
                             phone = "987-654-3210")

doc.add_item(Item("Product 1", "A product", 4, 30000))

doc.set_item_tax_rate(20)

doc.set_bottom_tip("Thank you for your business!")

doc.finish()