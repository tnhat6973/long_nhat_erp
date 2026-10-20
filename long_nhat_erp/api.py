import re

import frappe
from frappe.rate_limiter import rate_limit

PHONE_RE = re.compile(r"^[0-9+\-\s]{8,15}$")


def _clean(value, maxlen=500):
    return (value or "").strip()[:maxlen]


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=10, seconds=60)
def submit_contact(full_name, email, phone, message):
    full_name, email = _clean(full_name, 140), _clean(email, 140)
    phone, message = _clean(phone, 20), _clean(message, 2000)
    if not (full_name and email and message):
        frappe.throw("Vui lòng nhập đầy đủ họ tên, email và nội dung")
    frappe.utils.validate_email_address(email, throw=True)
    doc = frappe.get_doc({
        "doctype": "Contact Feedback", "full_name": full_name,
        "email": email, "phone": phone, "message": message,
    }).insert(ignore_permissions=True)
    return {"name": doc.name}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=10, seconds=60)
def place_order(customer_name, phone, address, item, qty, note=""):
    customer_name, phone = _clean(customer_name, 140), _clean(phone, 20)
    address, note = _clean(address, 500), _clean(note, 500)
    if not (customer_name and address):
        frappe.throw("Vui lòng nhập tên và địa chỉ giao hàng")
    if not PHONE_RE.match(phone):
        frappe.throw("Số điện thoại không hợp lệ")
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        frappe.throw("Số lượng không hợp lệ")
    if qty < 1 or qty > 1000:
        frappe.throw("Số lượng phải từ 1 đến 1000")

    # Giá lấy từ CSDL, không tin giá do trình duyệt gửi lên
    it = frappe.db.get_value("Item", item, ["item_name", "standard_rate", "disabled"], as_dict=True)
    if not it or it.disabled:
        frappe.throw("Sản phẩm không tồn tại hoặc đã ngừng bán")

    doc = frappe.get_doc({
        "doctype": "Online Order", "customer_name": customer_name, "phone": phone,
        "address": address, "item": item, "item_name": it.item_name,
        "qty": qty, "rate": it.standard_rate, "note": note,
    }).insert(ignore_permissions=True)
    return {"name": doc.name, "amount": doc.amount}
