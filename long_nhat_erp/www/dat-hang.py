import frappe


def get_context(context):
    context.no_cache = 1
    context.title = "Đặt hàng"
    context.items = frappe.get_all(
        "Item",
        filters={"disabled": 0, "item_code": ["like", "GD-%"]},
        fields=["item_code", "item_name", "standard_rate"],
        order_by="item_code",
    )
    context.selected = frappe.form_dict.get("item") or ""
