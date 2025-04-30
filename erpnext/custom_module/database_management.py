import csv
import io
import frappe
from frappe import _


@frappe.whitelist()
def import_csv():
    file1 = frappe.local.request.files.get("file1")
    file2 = frappe.local.request.files.get("file2")
    file3 = frappe.local.request.files.get("file3")

    if not file1 or not file2 or not file3:
        return {"status": "error", "message": "One or many file(s) are missing."}
            
    [data_file1, error_file1] = read_csv(file1)
    [data_file2, error_file2] = read_csv(file2)
    [data_file3, error_file3] = read_csv(file3)
    
    errors = error_file1 + error_file2 + error_file3
    errors = "".join(errors)
    if len(errors)!=0:
        print(str(errors))
        return {"status": "error", "message": f"<ul>{str(errors)}</ul>"} 
    
    # insert_data()
    return {"status": "success", "message": f"File received successfuly."}



def read_csv(file):
    content = file.stream.read().decode("utf-8")
    # csv_reader = csv.reader(io.StringIO(content))
    csv_reader = csv.reader(io.StringIO(content), delimiter=';')

    errors = []
    rows = []
    lines = []
    column_nb = 0        # column number per line
    for row_index, row in enumerate(csv_reader):
        if row_index == 0:
            column_nb = len(row)
        else:
            if column_nb != len(row):
                errors.append(f"<li>Column number is different at line {row_index+1}.</li>\n")
            else:
                for cell_index, cell in enumerate(row):
                    converted_value, errors = check_data_error(cell, errors, row_index, cell_index)
                    lines.append(converted_value)
                rows.append(lines)
                lines = []
    errors = [f'<br><p style="font-weight:bold; font-size: 16px;">File: {file.filename}</p>']+errors  if len(errors) != 0 else []
    
    print(f"\nTitle file : {file}")
    print(f"Data :\n {rows}")
    print(f"Errors :\n {errors}\n")
    
    return rows, errors
    
    
    
"""
    This function convert the cell data from the csv into his corresponding value
    and check if there are data errors (date format, negative value, None value, ....)
"""
def check_data_error(value, errors, row_index, cell_index): 
    value = value.strip()
    if value == "":
        errors.append(f"<li>No value, at line {row_index+1}, column {cell_index+1}.</li>\n")
        return None
    try:
        value = int(value)
        if value <= 0:
            errors.append(f"<li>Negative int value, at line {row_index+1}, column {cell_index+1}.</li>\n")
    except ValueError:
        try:
            value = float(value)
            if value <= 0:
                errors.append(f"<li>Negative float value, at line {row_index+1}, column {cell_index+1}.</li>\n")
        except ValueError:
            pass
            # if not has_date_format(value):
            #     errors.append(f"- Wrong date format at line {row_index}, column {cell_index}.")
    return value, errors



@frappe.whitelist()
def reset_database():
    # modules = frappe.get_all("Module Def", filters={"is_custom": 0}, fields=["name"])
    # doctypes = [""]
    modules = ["custom-module"]
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
    
    