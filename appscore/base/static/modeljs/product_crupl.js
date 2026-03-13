document.addEventListener('DOMContentLoaded', async () => {

    const form = document.getElementById('formGeneric');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const actionhtml = document.getElementById('action').value;

    let supplierOptions = [];

    // cargar supplier en conbo
    async function loadSuppliers() {
        const response = await fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ action: 'get_suppliers' })
        });

        supplierOptions = await response.json();

        // llenar select del modal
        const select = document.getElementById('modalSupplier');
        select.innerHTML = '<option value="">Seleccione</option>';

        supplierOptions.forEach(p => {
            select.innerHTML += `<option value="${p.id}">${p.name}</option>`;
        });
    }

    // construir combo tabla
    function buildSupplierSelect(selectedId = '') {
        let html = `<select class="form-select form-select-sm input-supplier">`;
        html += `<option value="">Seleccione</option>`;

        supplierOptions.forEach(p => {
            const selected = p.id == selectedId ? 'selected' : '';
            html += `<option value="${p.id}" ${selected}>${p.name}</option>`;
        });

        html += `</select>`;
        return html;
    }

    // obtener líneas
    function getSupplierLines() {
        const rows = document.querySelectorAll('#datatableid tbody tr');
        const lines = [];

        rows.forEach(row => {
            const supplier = row.querySelector('.input-supplier')?.value;
            const price = row.querySelector('.input-price')?.value;

            if (supplier) {
                lines.push({
                    partner_id: supplier,
                    price: parseInt(price || 1)
                });
            }
        });

        return lines;
    }

    // submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const headData = Object.fromEntries(formData.entries());
        headData.lines = getSupplierLines();

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
            window.location.href = "/base/product/list/";
        } else {
            console.error(data.error);
        }
    });

    await loadSuppliers();

    // datatable
    const table = new DataTable('#datatableid', {
        data: [],
        columns: [
            { data: null },
            { data: 'partner_id' },
            { data: 'price' },
            { data: null }
        ],
        columnDefs: [
            {
                targets: 0,
                render: (data, type, row, meta) => meta.row + 1
            },
            {
                targets: 1,
                render: (data) => buildSupplierSelect(data)
            },
            {
                targets: 2,
                render: (data) => `
                    <input type="number" min="1"
                    class="form-control form-control-sm input-price"
                    value="${data ?? 1}">
                `
            },
            {
                targets: 3,
                render: () => `
                    <button class="btn btn-danger btn-sm btn-delete">✕</button>
                `
            }
        ]
    });

    // cargar líneas en edit
    async function loadSupplierLines() {
        const response = await fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ action: 'get_lines' })
        });

        const lines = await response.json();
        table.rows.add(lines).draw();
    }

    if (actionhtml === 'edit') {
        await loadSupplierLines();
    }

    document.getElementById('btnSaveLine').addEventListener('click', () => {

        const partner = document.getElementById('modalSupplier').value;
        const price = document.getElementById('modalPrice').value;

        if (!partner) {
            alert("Seleccione el proveedor");
            return;
        }

        table.row.add({
            partner_id: partner,
            price: price
        }).draw(false);

        const modal = bootstrap.Modal.getInstance(document.getElementById('lineModal'));
        modal.hide();

        document.getElementById('modalSupplier').value = '';
        document.getElementById('modalPrice').value = 1;
    });

    document.querySelector('#datatableid tbody').addEventListener('click', e => {
        if (e.target.classList.contains('btn-delete')) {
            table.row(e.target.closest('tr')).remove().draw();
        }
    });

});