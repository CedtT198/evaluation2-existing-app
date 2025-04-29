import csv
import io
import frappe
from frappe import _


@frappe.whitelist()
def import_csv():
    file1 = frappe.local.request.files.get("file1")
    file2 = frappe.local.request.files.get("file2")
    file3 = frappe.local.request.files.get("file3")

    if not file1 and not file2 and not file3:
        return {"status": "error", "message": "One or many file(s) are missing."}
            
    try:
        data_file1 = read_csv(file1)
        data_file2 = read_csv(file2)
        data_file3 = read_csv(file3)
    except Exception as e:
        print(str(e))
        return {"status": "error", "message": str(e)} 
    return {"status": "success", "message": f"File received successfuly."}


def read_csv(file):
    content = file.stream.read().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(content))

    rows = []
    for row in csv_reader:
        rows.append(row)
    
    print(f"\nTitle file : {file}")
    print(f"Data :\n {rows}\n")
    
    return rows



@frappe.whitelist()
def reset_database():
    # modules = frappe.get_all("Module Def", filters={"is_custom": 0}, fields=["name"])
    # doctypes = [""]
    modules = ["custom-module", "Buying"]
    for module in modules:
        doctypes_in_module = frappe.get_all("DocType", filters={"module": module}, fields=["name"])
        for doctype in doctypes_in_module:
        # for doctype in doctypes:
            table_name = f"{doctype.name}"
            
            if frappe.db.table_exists(table_name):
                try:
                    frappe.db.truncate(table_name)            
                    print(f"{table_name} truncated.")
                except Exception as e:
                    frappe.log_error(frappe.get_traceback(), _("Error truncating table"))
                    frappe.msgprint(_(f"Failed to truncate table {table_name}: {str(e)}"))
    frappe.msgprint(_(f"Tables {modules} truncated successfulty."))
    
    

