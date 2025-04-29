frappe.pages['database-management'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Database Management',
		single_column: true
	});

    const html = `
        <div class="container" style="margin-top: 25px;">
            <div class="row">
                <div class="col-md-6">
					<div style="margin-left: 25px; margin-bottom: 25px;">
						<div style="margin-bottom: 25px;">
							<p style="font-weight:bold; font-size: 22px;">Import</p>
							<p>Choose the csv files.</p>
						</div>
						<form class="offset-md-1" style="margin-bottom: 25px;">
							<div></div>
							<div class="input-group mb-3">
								<label for="file1">File 1</label>
								<input type="file" id="file1">
							</div>
							<div class="input-group mb-3">
								<label for="file2">File 2</label>
								<input type="file" id="file2">
							</div>
							<div class="input-group mb-3">
								<label for="file3">File 3</label>
								<input type="file" id="file3">
							</div>
							<button class="btn btn-primary offset-md-8" id="import_csv">Import files</button>
						</form>
					</div>
                </div>
                <div class="col-md-6" style="border-left: 1px solid gray">
					<div style="margin-bottom: 25px;">
						<p style="font-weight:bold; font-size: 22px;">Reset</p>
	                    <p>This action will delete all the data in the database.</p>
					</div>
                    <button class="btn btn-primary" id="reset-db-btn">
                        Reset data in database
                    </button>
                </div>
            </div>
        </div>
    `;
	
    $(page.body).append(html);
    $('#import_csv').on('click', (event) => {
		event.preventDefault();	
        import_data_csv();
    });
    $('#reset-db-btn').on('click', (event) => {
		event.preventDefault();
        reset_database();
    });

	
// 	let container = $('<div>')
// 		.addClass('container')
// 		.css({ 'margin-top': '25px' })
// 		.appendTo(page.body);
		
// 	let row = $('<div>')
// 		.addClass('row')
// 		.appendTo(container);

// 	// left side
// 	let left = $('<div>')
// 		.addClass('col-md-6')
// 		.appendTo(row);
		
// 	let text1 = $('<p>')
// 		.text('Choose a csv file.')
//         .css({ 'margin-left': '25px' })
// 		.css({ 'margin-bottom': '25px' })
// 		.appendTo(left);

// 	// right side
//     let right = $('<div>')
// 		.addClass('col-md-6')
//         .appendTo(row);

// 	let text2 = $('<p>')
// 		.text('This action will reset the data in the database.')
//         .css({ 'margin-bottom': '25px' })
//         .appendTo(right);

//     let button = $('<button>')
//         .text('Reset data in database')
//         .addClass('btn btn-primary')
//         .css({ 'margin-left': '25px' })
//         .on('click', () => {
// 			reset_database();
//         })
//         .appendTo(right);
}



//  appel des api
import_data_csv = function() {
	const formData = new FormData();
    formData.append('file1', document.getElementById('file1').files[0]);
    formData.append('file2', document.getElementById('file2').files[0]);
    formData.append('file3', document.getElementById('file3').files[0]);

    fetch('/api/method/erpnext.custom_module.database_management.import_csv', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Frappe-CSRF-Token': frappe.csrf_token
        }
    })
    .then(res => res.json())
    .then(res => {
        if (res.message && res.message.status === "success") {
            frappe.msgprint("Import done !");
        } else {
            frappe.msgprint("Error : " + (res.message?.message || "Unkown"));
        }
    })
    .catch(err => {
        frappe.msgprint("Erreur réseau : " + err.message);
    });
}


reset_database = function() {
	frappe.confirm(__("Are you sure you want to clear the database ?"), () => {
		frappe.call({
			method: "erpnext.custom_module.database_management.reset_database",
			freeze: true,
			freeze_message: __("Clearing database..."),
			callback: function (r) {
                // // Afficher le message retourné par l'API
                // if (r.message) {
                //     frappe.msgprint(r.message);
                // } else {
                //     frappe.msgprint(__('Message.'));
                // }
				frappe.ui.toolbar.clear_cache();
				frappe.show_alert({
					message: __("Database cleared."),
					indicator: "green",
				});
			},
		});
	});
}