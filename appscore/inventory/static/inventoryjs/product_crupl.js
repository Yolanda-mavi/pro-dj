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

    const typeField = document.getElementById('id_type');
    typeField.addEventListener('change', toggleExtraField);
    toggleExtraField();
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
            body: JSON.stringify({ action: 'get_suppliers' })
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
    function addLine() {
        lines.push({
            id: null,
            partner_id: '',
            price: ''
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
                            <option value="${p.id}" ${p.id == line.partner_id ? 'selected' : ''}>
                                ${p.name}
                            </option>
                        `).join('')}
                    </select>
                    <div class="text-danger small error-partner"></div>
                </td>
                <td>
                    <input type="number" class="form-control form-control-sm input-price" value="${line.price}">
                    <div class="text-danger small error-price"></div>
                </td>
                <td>
                    <button class="btn btn-danger btn-sm btn-delete">✕</button>
                </td>
            `;
            tbody.appendChild(tr);
            const select = tr.querySelector('.tomselect');
            initTomSelect(select);

            tr.querySelector('.input-partner').addEventListener('change', e => {
                line.partner_id = e.target.value;
                validateLine(line, tr);
            });

            tr.querySelector('.input-price').addEventListener('input', e => {
                line.price = e.target.value;
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

        if (!line.partner_id) {
            row.querySelector('.error-partner').textContent = "Requerido";
            valid = false;
        } else {
            row.querySelector('.error-partner').textContent = "";
        }

        if (!line.price || parseFloat(line.price) <= 0) {
            row.querySelector('.error-price').textContent = "Precio inválido";
            valid = false;
        } else {
            row.querySelector('.error-price').textContent = "";
        }

        const duplicates = lines.filter(l => l.partner_id === line.partner_id);
        if (line.partner_id && duplicates.length > 1) {
            row.querySelector('.error-partner').textContent = "Proveedor duplicado";
            valid = false;
        }

        return valid;
    }

    function validateAll() {
        return lines.every(line => {
            return line.partner_id && line.price > 0;
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
            window.location.href = "/base/product/list/";
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
            partner_id: l.partner_id,
            price: l.price
        }));

        renderTable();
    }

    document.getElementById('btnAddLine').addEventListener('click', () => {
        addLine();
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