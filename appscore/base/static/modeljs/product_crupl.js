document.addEventListener('DOMContentLoaded', async () => {

    const form = document.getElementById('formGeneric');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const actionhtml = document.getElementById('action').value;
    //para pocos registros
    function initTomSelect(element) {
    if (!element || element.tomselect) return;

    new TomSelect(element, {
        create: false,
        maxOptions: 200,
        placeholder: "Buscar...",
        allowEmptyOption: true
    });
    }

    const typeField = document.getElementById('id_type');
    typeField.addEventListener('change', toggleExtraField);
    toggleExtraField();


    // new TomSelect("#id_fraction_mx", {
    // valueField: "id",
    // labelField: "name",
    // searchField: "name",
    //
    // load: async function(query, callback) {
    //     if (!query.length) return callback();
    //
    //     const res = await fetch(`/api/fraction/?q=${query}`);
    //     const data = await res.json();
    //     callback(data);
    // }
    // });
    //
    // new TomSelect("#id_fraction_htsus", {
    // valueField: "id",
    // labelField: "name",
    // searchField: "name",
    //
    // load: async function(query, callback) {
    //     if (!query.length) return callback();
    //
    //     const res = await fetch(`/api/fraction/?q=${query}`);
    //     const data = await res.json();
    //     callback(data);
    // }
    // });
    // initTomSelect(document.getElementById('id_combos'), {
    // valueField: "id",
    // labelField: "name",
    // searchField: "name",
    //
    // load: async function(query, callback) {
    //     if (!query.length) return callback();
    //
    //     const res = await fetch(`/api/fraction/?q=${query}`);
    //     const data = await res.json();
    //     callback(data);
    // }
    // });

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
                window.location.href = "/base/product/list/";
                //window.location.href = '{{ list_url }}';
            } else {
                //console.error(data.error);
                show_errors_toast(data.error);
                //show_field_errors(data.error);
            }
        }catch(e){
            console.error(e);
            show_errors_toast(e);
            //show_field_errors(e);
        }

    });

    await loadSuppliers();

    initTomSelect(document.getElementById('id_fraction_mx'));
    initTomSelect(document.getElementById('id_fraction_htsus'));
    initTomSelect(document.getElementById('id_sector'));
    initTomSelect(document.getElementById('id_fraction_us'));
    initTomSelect(document.getElementById('id_country'));
    initTomSelect(document.getElementById('id_fraction_us_exp'));
    initTomSelect(document.getElementById('id_category'));
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

    function updateCost() {
        const id_cav_ind = parseFloat(document.getElementById('id_cav_ind').value) || 0;
        const id_cav_dir = parseFloat(document.getElementById('id_cav_dir').value) || 0;
        const id_cav_nat = parseFloat(document.getElementById('id_cav_nat').value) || 0;
        document.getElementById('id_cost_av').value = (id_cav_ind + id_cav_dir + id_cav_nat).toFixed(4);
        const id_uc_mat_or = parseFloat(document.getElementById('id_uc_mat_or').value) || 0;
        const id_uc_pack_or = parseFloat(document.getElementById('id_uc_pack_or').value) || 0;
        document.getElementById('id_uc_or_stot').value = (id_uc_pack_or + id_uc_mat_or).toFixed(4);
        const id_uc_mat_nor = parseFloat(document.getElementById('id_uc_mat_nor').value) || 0;
        const id_uc_pack_nor = parseFloat(document.getElementById('id_uc_pack_nor').value) || 0;
        document.getElementById('id_uc_nor_stot').value = (id_uc_mat_nor + id_uc_pack_nor).toFixed(4);

        document.getElementById('id_cost').value = (id_uc_mat_nor + id_uc_pack_nor+id_uc_pack_or+id_uc_mat_or).toFixed(4);
        document.getElementById('id_cost_tot').value = (id_uc_mat_nor + id_uc_pack_nor+id_uc_pack_or+id_uc_mat_or+id_cav_ind + id_cav_dir + id_cav_nat).toFixed(4);

    }
    document.getElementById('id_cav_ind').addEventListener('input', updateCost);
    document.getElementById('id_cav_dir').addEventListener('input', updateCost);
    document.getElementById('id_cav_nat').addEventListener('input', updateCost);
    document.getElementById('id_uc_mat_or').addEventListener('input', updateCost);
    document.getElementById('id_uc_mat_nor').addEventListener('input', updateCost);
    document.getElementById('id_uc_pack_or').addEventListener('input', updateCost);
    document.getElementById('id_uc_pack_nor').addEventListener('input', updateCost);

    function toggleExtraField() {
        const value = document.getElementById('id_type').value;
        const div = document.getElementById('costTabContent');

        if ( value === 'F' ) {
            div.classList.remove('d-none');
        } else {
            div.classList.add('d-none');
        }
    }


});