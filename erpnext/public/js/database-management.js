frappe.pages['ma-page-boutons'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Ma Page avec Boutons',
        single_column: true
    });

    // Créer deux boutons
    page.add_inner_button('Bouton 1', () => {
        frappe.msgprint('Tu as cliqué sur Bouton 1');
    });

    page.add_inner_button('Bouton 2', () => {
        frappe.msgprint('Tu as cliqué sur Bouton 2');
    });
};
