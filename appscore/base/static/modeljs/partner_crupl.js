
document.addEventListener('DOMContentLoaded', async () => {

    const form = document.getElementById('formGeneric');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let productOptions = [];

    // Cargar productos desde Django
    async function loadProducts() {
        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ action: 'get_products' })
            });

            productOptions = await response.json();

        } catch (err) {
            console.error("Error cargando productos", err);
        }
    }

    //  Construir combo
    function buildProductSelect(selectedId = '') {
        let html = `<select class="form-select form-select-sm input-product">`;
        html += `<option value="">Seleccione</option>`;

        productOptions.forEach(p => {
            const selected = p.id == selectedId ? 'selected' : '';
            html += `<option value="${p.id}" ${selected}>${p.name}</option>`;
        });

        html += `</select>`;
        return html;
    }

    async function loadBomLines() {
    try {
        const response = await fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ action: 'get_lines' })
        });

        const lines = await response.json();

        table.clear();
        table.rows.add(lines).draw();

    } catch (err) {
        console.error("Error cargando líneas", err);
    }
    }

    //  Leer detalle
    function getBomLines() {
        const rows = document.querySelectorAll('#datatableid tbody tr');
        const lines = [];

        rows.forEach(row => {
            const product = row.querySelector('.input-product')?.value;
            const quantity = row.querySelector('.input-qty')?.value;

            if (product) {
                lines.push({
                    product: product,
                    quantity: parseInt(quantity || 1)
                });
            }
        });

        return lines;
    }

    // Submit HEAD + DETAIL
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const headData = Object.fromEntries(formData.entries());

        headData.lines = getBomLines();
        console.log(getBomLines())

        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(headData)
            });

            const data = await response.json();

            if (data.success) {
                window.location.href = "/base/bom/list/";
                //window.location.href = "{{ list_url }}";
            } else {
                //console.error("Errores:", data.error);
                show_errors_toast(data.error);
                //show_field_errors(data.error);
            }

        } catch (err) {
            //console.error("Error en submit", err);
            show_errors_toast(err);
            //show_field_errors(err);
        }
    });

    // Esperar productos antes de crear tabla
    await loadProducts();

    //  DataTable
    const table = new DataTable('#datatableid', {
        data: [],
        columns: [
            { data: null },
            { data: 'product_id' },
            { data: 'quantity' },
            { data: null }
        ],
        columnDefs: [
            {
                targets: 0,
                render: (data, type, row, meta) => meta.row + 1
            },
            {
                targets: 1,
                render: (data) => buildProductSelect(data)
            },
            {
                targets: 2,
                render: (data) => `
                    <input type="number"
                           min="1"
                           class="form-control form-control-sm input-qty"
                           value="${data ?? 1}">
                `
            },
            {
                targets: 3,
                render: () => `
                    <button type="button" class="btn btn-danger btn-sm btn-delete">
                        ✕
                    </button>
                `
            }
        ]
    });

    // const formData_action = new FormData(form);
    // const headData_action = Object.fromEntries(formData_action.entries());
    //
    // headData_action.action = getBomLines();
    const actionhtml = document.getElementById('action').value;

    if (actionhtml === 'edit') {
        await loadBomLines();
    }

    //  Agregar línea
    document.getElementById('btnAddLine').addEventListener('click', () => {
        table.row.add({
            product_id: '',
            quantity: 1
        }).draw(false);
    });

    //Eliminar línea
    document.querySelector('#datatableid tbody').addEventListener('click', e => {
        if (e.target.classList.contains('btn-delete')) {
            table.row(e.target.closest('tr')).remove().draw();
        }
    });


});



