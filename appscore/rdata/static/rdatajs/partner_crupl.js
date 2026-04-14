document.addEventListener('DOMContentLoaded', async () => {

    const form = document.getElementById('formGeneric');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const actionhtml = document.getElementById('action').value;

   function initTomSelect(element, options = {}) {
    if (!element || element.tomselect) return;
        new TomSelect(element, {
            create: false,
            maxOptions: 200,
            placeholder: "Buscar...",
            allowEmptyOption: true,
            ...options
        });
    }

    document.querySelectorAll('.tomselect').forEach(el => {
        initTomSelect(el);
    });
    let lines = [];
    let partnerOptions = [];
    let currentPage = 1;
    let rowsPerPage = 10;

    async function loadPartners() {
        try{
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ action: 'get_partners' })
            });

            partnerOptions = await response.json();
        } catch (err) {
            console.error("Error cargando contactos", err);
        }
    }

//    function addLine(data = {}) {
//        const line = {
//            id: data.id || null,
//            partner_id: data.partner_id || '',
//            price: data.price || '',
//            _isNew: !data.id
//        };
//
//        lines.push(line);
//        renderTable();
//    }
   /* function addLine() {
        lines.push({
            id: null,
            partner_id: '',
            price: ''
        });

        currentPage = Math.ceil(lines.length / rowsPerPage);
        renderTable();
    }*/

    function addLine() {
        lines.push({
            id: '',
        });

        currentPage = Math.ceil(lines.length / rowsPerPage);
        renderTable();
    }

    function renderPagination() {
        const container = document.getElementById('pagination');
        container.innerHTML = '';
        const totalPages = Math.ceil(lines.length / rowsPerPage);

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            btn.className = 'btn btn-sm ' + (i === currentPage ? 'btn-primary' : 'btn-light');

            btn.addEventListener('click', () => {
                currentPage = i;
                renderTable();
            });

            container.appendChild(btn);
        }
    }

    await loadPartners();

    if (actionhtml === 'edit') {
        await loadLines();
    }else{
        renderTable();
    }

    function renderTable() {
        const tbody = document.querySelector('#datatableid tbody');
        tbody.innerHTML = '';

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const paginatedLines = lines.slice(start, end);

        paginatedLines.forEach((line, index) => {
            const realIndex = start + index;

            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${realIndex + 1}</td>
                <td>
                    <select class="input-partner tomselect ">
                        <option value="">Seleccione</option>
                        ${partnerOptions.map(p => `
                            <option value="${p.id}" ${p.id == line.id ? 'selected' : ''}>
                                ${p.name}
                            </option>
                        `).join('')}
                    </select>
                    <div class="text-danger small error-partner"></div>
                </td>
                <td>
                    <button class="btn btn-danger btn-sm btn-delete">✕</button>
                </td>
            `;
            tbody.appendChild(tr);
            const select = tr.querySelector('.tomselect');
            initTomSelect(select);

            tr.querySelector('.input-partner').addEventListener('change', e => {
                line.id = e.target.value;
                validateLine(line, tr);
            });

            tr.querySelector('.btn-delete').addEventListener('click', () => {
                lines.splice(realIndex, 1);
                renderTable();
            });


        });

        renderPagination();
    }

    function validateLine(line, row) {
        let valid = true;

        if (!line.id) {
            row.querySelector('.error-partner').textContent = "Requerido";
            valid = false;
        } else {
            row.querySelector('.error-partner').textContent = "";
        }


        const duplicates = lines.filter(l => l.id === line.id);
        if (line.id && duplicates.length > 1) {
            row.querySelector('.error-partner').textContent = "Contacto duplicado";
            valid = false;
        }

        return valid;
    }

    function validateAll() {
        return lines.every(line => {
            return line.id;
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateAll()) {
            alert("Corrige los errores");
            return;
        }

        const formData = new FormData(form);
        const headData = Object.fromEntries(formData.entries());

        headData.lines = lines;

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
            window.location.href = "/base/partner/list/";
        } else {
            show_errors_toast(data.error);
        }
    });

    async function loadLines() {
        const response = await fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ action: 'get_lines' })
        });

        const data = await response.json();

        lines = data.map(l => ({
            id: l.id,
        }));

        renderTable();
    }

    document.getElementById('btnAddLine').addEventListener('click', () => {
        addLine();
    });


});




////////////////////////////////////////////////////////////////////////////
/*
document.addEventListener('DOMContentLoaded', async () => {

    const form = document.getElementById('formGeneric');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let partnerOptions = [];

     function initDatePickers() {
        flatpickr(
            document.querySelectorAll(".datepicker:not(.flatpickr-input)"),
            {
                dateFormat: "Y-m-d",
            }
        );
    }

    initDatePickers();

    document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', initDatePickers);
    });


    function initTomSelect(element, options = {}) {
    if (!element || element.tomselect) return;
        new TomSelect(element, {
            create: false,
            maxOptions: 200,
            placeholder: "Buscar...",
            allowEmptyOption: true,
            ...options
        });
    }

    async function loadPartner() {
        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ action: 'get_partners' })
            });

            partnerOptions = await response.json();

        } catch (err) {
            console.error("Error cargando contactos", err);
        }
    }


    function buildPartnerSelect(selectedId = '') {
        let html = `<select class="form-select form-select-sm input-partner">`;
        html += `<option value="">Seleccione</option>`;

        partnerOptions.forEach(p => {
            const selected = p.id == selectedId ? 'selected' : '';
            html += `<option value="${p.id}" ${selected}>${p.name}</option>`;
        });

        html += `</select>`;
        return html;
    }

    async function loadPartnerLines() {
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

    function getPartnerLines() {
        const rows = document.querySelectorAll('#datatableid tbody tr');
        const lines = [];

        rows.forEach(row => {
            const partner = row.querySelector('.input-partner')?.value;

            if (partner) {
                lines.push({
                    partner: partner
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

        headData.lines = getPartnerLines();


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
                window.location.href = "/base/partner/list/";
                console.log("entro a")
                //window.location.href = "{{ list_url }}";
            } else {
            console.log(data.error)
                //console.error("Errores:", data.error);
                show_errors_toast(data.error);
                //show_field_errors(data.error);
            }

        } catch (err) {
        console.log("err")
            //console.error("Error en submit", err);
            show_errors_toast(err);
            //show_field_errors(err);
        }
    });

    // Esperar productos antes de crear tabla
    await loadPartner();


    document.querySelectorAll('.tomselect').forEach(el => {
        initTomSelect(el);
    });

    //  DataTable
    const table = new DataTable('#datatableid', {
        data: [],
        columns: [
            { data: null },
            { data: 'id' },

            { data: null }
        ],
        columnDefs: [
            {
                targets: 0,
                render: (data, type, row, meta) => meta.row + 1
            },

            {
            targets: 1,
            render: (data, type, row) => buildPartnerSelect(row.id)
            },


            {
                targets: 2,
                render: () => `
                    <button type="button" class="btn btn-danger btn-sm btn-delete">
                        ✕
                    </button>
                `
            }
        ],

    });


    const actionhtml = document.getElementById('action').value;

    if (actionhtml === 'edit') {
        await loadPartnerLines();
    }

    document.getElementById('btnAddLine').addEventListener('click', () => {
        table.row.add({
            id: '',

        }).draw(false);
    });

    document.querySelector('#datatableid tbody').addEventListener('click', e => {
        if (e.target.classList.contains('btn-delete')) {
            table.row(e.target.closest('tr')).remove().draw();
        }
    });





});

*/

