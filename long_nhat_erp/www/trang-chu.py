import frappe


def get_context(context):
    context.no_cache = 1
    context.title = "Long Nhật - Gia dụng thông minh"
    rows = frappe.get_all(
        "Item",
        filters={"disabled": 0, "item_code": ["like", "GD-%"]},
        fields=["item_code", "item_name", "description", "standard_rate"],
        order_by="item_code",
    )
    for r in rows:
        r.price_text = "{:,.0f} ₫".format(r.standard_rate or 0).replace(",", ".")
    context.items = rows
