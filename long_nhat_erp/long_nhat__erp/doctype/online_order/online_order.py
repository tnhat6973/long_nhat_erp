import frappe
from frappe.model.document import Document


class OnlineOrder(Document):
    def validate(self):
        if (self.qty or 0) < 1:
            frappe.throw("Số lượng phải lớn hơn 0")
        self.amount = (self.qty or 0) * (self.rate or 0)
