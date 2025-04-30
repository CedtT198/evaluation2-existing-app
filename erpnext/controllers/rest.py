# only the api rest controller here

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def test_api():
    print("\nAPI RIGHT THERE\n")
    return "API RIGHT THERE"