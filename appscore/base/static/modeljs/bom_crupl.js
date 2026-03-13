
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
            } else {
                console.error("Errores:", data.error);
            }

        } catch (err) {
            console.error("Error en submit", err);
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

/*
document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('formGeneric');

    // función para leer las líneas del detalle
    function getBomLines() {
        const rows = document.querySelectorAll('#datatableid tbody tr');
        const data = [];

        rows.forEach(row => {
            data.push({
                product: row.querySelector('.input-product')?.value || '',
                quantity: row.querySelector('.input-qty')?.value || 0
            });
        });

        return data;
    }

    // submit del form (HEAD + DETAIL)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const headData = Object.fromEntries(formData.entries());

        headData.lines = getBomLines(); // 👈 aquí se usa

        const response = await fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(headData)
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = "/base/bom/list/";
        } else {
            console.log(data.error);
        }
    });


    // DataTable
    const table = new DataTable('#datatableid', {
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            data: () => JSON.stringify({ action: 'searchdata' }),
            dataSrc: ""
        },
        columns: [
            { data: null },
            { data: 'product_name' },
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
                render: (data) => `
                    <input class="form-control form-control-sm input-product"
                           value="${data ?? ''}">
                `
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
                render: () => `<button class="btn btn-danger btn-sm btn-delete">X</button>`
            }
        ]
    });

    // agregar fila
    document.getElementById('btnAddLine').addEventListener('click', () => {
        table.row.add({
            id: null,
            product_name: '',
            quantity: 1
        }).draw(false);
    });

    // eliminar fila
    document.querySelector('#datatableid tbody').addEventListener('click', e => {
        if (e.target.classList.contains('btn-delete')) {
            table.row(e.target.closest('tr')).remove().draw();
        }
    });

});*/

/*
document.addEventListener('DOMContentLoaded', () => {

    let bomLines = []; //  almacena el detalle en memoria

    const table = new DataTable('#datatableid', {
        data: bomLines,
        columns: [
            { data: null },
            { data: 'product_name' },
            { data: 'quantity' },
            {
                data: null,
                render: function (data, type, row, meta) {
                    return `<button class="btn btn-danger btn-sm btnRemove" data-index="${meta.row}">
                                Eliminar
                            </button>`;
                }
            }
        ],
        columnDefs: [{
            targets: 0,
            render: (data, type, row, meta) => meta.row + 1
        },
        //     {
        // targets: 1,
        // render: function (data, type, row) {
        //     return '<input type="number" min="1" class="form-control form-control-sm input-qty" value="${row.quantity}" data-id="${row.id}">';
        // }
        // },
            {
        targets: 2,
        render: function (data, type, row) {
            return '<input type="number" min="1" class="form-control form-control-sm input-qty" value="${row.quantity}" data-id="${row.id}">';
        }
    }
        ]
    });

    // Agregar línea (ejemplo simple)
    document.getElementById('btnAddLine').addEventListener('click', () => {
        console.log("linea 29---");
        // const productId = prompt("ID producto34");
        // const productName = prompt("Nombre producto111");
        // const quantity = prompt("Cantidad111");
        //
        // if (!productId || !quantity) return;
        //
        // bomLines.push({
        //     product_id: productId,
        //     product_name: productName,
        //     quantity: quantity
        // });

        bomLines.push({
            product_id: null,
            product_name: null,
            quantity: 1
        });

        table.clear().rows.add(bomLines).draw();
    });

    // eliminar línea
    document.querySelector('#datatableid tbody').addEventListener('click', (e) => {
        if (e.target.classList.contains('btnRemove')) {
            const index = e.target.dataset.index;
            bomLines.splice(index, 1);
            table.clear().rows.add(bomLines).draw();
        }
    });

    // submit
    document.getElementById('formGeneric').addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const headData = Object.fromEntries(formData.entries());

        const payload = {
            action: headData.action,
            head: headData,
            detail: bomLines
        };

        const response = await fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            console.log(data.error);
        }
    });

});*/