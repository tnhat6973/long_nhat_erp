import os
import frappe

MODULE = open(os.path.join(os.path.dirname(__file__), "modules.txt")).read().splitlines()[0].strip()

PERMS = [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1,
     "report": 1, "export": 1, "share": 1, "print": 1, "email": 1},
    {"role": "Sales User", "read": 1, "write": 1, "create": 1, "delete": 1,
     "report": 1, "print": 1, "email": 1},
]
STATUS = "New\nConfirmed\nDelivered\nCancelled"


def make(name, prefix, fields):
    if frappe.db.exists("DocType", name):
        print("Da co:", name)
        return
    frappe.get_doc({
        "doctype": "DocType", "name": name, "module": MODULE, "custom": 0,
        "naming_rule": "Expression", "autoname": f"format:{prefix}-{{#####}}",
        "sort_field": "modified", "sort_order": "DESC", "track_changes": 1,
        "fields": fields, "permissions": PERMS,
    }).insert(ignore_permissions=True)
    print("Da tao:", name)


def run():
    make("Contact Feedback", "LH", [
        {"fieldname": "full_name", "fieldtype": "Data", "label": "Họ tên", "reqd": 1, "in_list_view": 1},
        {"fieldname": "email", "fieldtype": "Data", "options": "Email", "label": "Email", "reqd": 1, "in_list_view": 1},
        {"fieldname": "phone", "fieldtype": "Data", "options": "Phone", "label": "Số điện thoại"},
        {"fieldname": "message", "fieldtype": "Small Text", "label": "Nội dung", "reqd": 1},
        {"fieldname": "status", "fieldtype": "Select", "label": "Trạng thái",
         "options": "New\nRead\nReplied", "default": "New", "in_list_view": 1},
    ])
    make("Online Order", "DH", [
        {"fieldname": "customer_name", "fieldtype": "Data", "label": "Tên khách hàng", "reqd": 1, "in_list_view": 1},
        {"fieldname": "phone", "fieldtype": "Data", "options": "Phone", "label": "Số điện thoại", "reqd": 1},
        {"fieldname": "address", "fieldtype": "Small Text", "label": "Địa chỉ giao hàng", "reqd": 1},
        {"fieldname": "item", "fieldtype": "Link", "options": "Item", "label": "Sản phẩm", "reqd": 1},
        {"fieldname": "item_name", "fieldtype": "Data", "label": "Tên sản phẩm", "read_only": 1, "in_list_view": 1},
        {"fieldname": "qty", "fieldtype": "Int", "label": "Số lượng", "reqd": 1, "default": "1", "in_list_view": 1},
        {"fieldname": "rate", "fieldtype": "Currency", "label": "Đơn giá", "read_only": 1},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Thành tiền", "read_only": 1},
        {"fieldname": "note", "fieldtype": "Small Text", "label": "Ghi chú"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Trạng thái",
         "options": STATUS, "default": "New", "in_list_view": 1},
    ])
    frappe.db.commit()
