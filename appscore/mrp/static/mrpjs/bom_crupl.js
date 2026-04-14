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
    let productOptions = [];

    let visibleCount = 10;
    const increment = 10;
    let observer;


    async function loadProducts() {
        try{
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

    function addLine() {
        lines.push({
            id: null,
            product_id: '',
            quantity: 1.0
        });

        visibleCount = lines.length;
        renderTable();
    }

    await loadProducts();

    if (actionhtml === 'edit') {
        await loadLines();
    }else{
        renderTable();
    }
    function renderTable() {
        const tbody = document.querySelector('#datatableid tbody');
        tbody.innerHTML = '';

        const visibleLines = lines.slice(0, visibleCount);

        visibleLines.forEach((line, index) => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${index + 1}</td>

                <td>
                    <select class="input-product tomselect">
                        <option value="">Seleccione</option>
                        ${productOptions.map(p => `
                            <option value="${p.id}" ${p.id == line.product_id ? 'selected' : ''}>
                                ${p.name}
                            </option>
                        `).join('')}
                    </select>
                    <div class="text-danger small error-product"></div>
                </td>

                <td>
                    <input type="number" class="form-control form-control-sm input-quantity" value="${line.quantity}">
                    <div class="text-danger small error-quantity"></div>
                </td>

                <td>
                    <button class="btn btn-danger btn-sm btn-delete">✕</button>
                </td>
            `;
            tbody.appendChild(tr);
            const select = tr.querySelector('.tomselect');
            initTomSelect(select);

            tr.querySelector('.input-product').addEventListener('change', e => {
                line.product_id = e.target.value;
                validateLine(line, tr);
            });

            tr.querySelector('.input-quantity').addEventListener('input', e => {
                line.quantity = e.target.value;
                validateLine(line, tr);
            });

            tr.querySelector('.btn-delete').addEventListener('click', () => {
                lines.splice(index, 1);
                visibleCount = Math.min(visibleCount, lines.length);
                renderTable();
            });


        });

        const loading = document.getElementById('loading');
        if (loading) {
            if (visibleCount >= lines.length) {
                loading.textContent = "No hay más registros";
            } else {
                loading.textContent = "Cargando...";
            }
        }

        renderObserver();
    }

    function validateLine(line, row) {
        let valid = true;

        if (!line.product_id) {
            row.querySelector('.error-product').textContent = "Requerido";
            valid = false;
        } else {
            row.querySelector('.error-product').textContent = "";
        }

        if (!line.quantity || parseFloat(line.quantity) <= 0) {
            row.querySelector('.error-quantity').textContent = "Precio inválido";
            valid = false;
        } else {
            row.querySelector('.error-quantity').textContent = "";
        }

        const duplicates = lines.filter(l => l.product_id === line.product_id);
        if (line.product_id && duplicates.length > 1) {
            row.querySelector('.error-product').textContent = "Producto duplicado";
            valid = false;
        }

        return valid;
    }

    function validateAll() {
        return lines.every(line => {
            return line.product_id && line.quantity > 0;
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
            window.location.href = "/base/bom/list/";
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
            product_id: l.product_id,
            quantity: l.quantity
        }));

        visibleCount = 10;

        renderTable();
    }

    document.getElementById('btnAddLine').addEventListener('click', () => {
        addLine();
    });

    function renderObserver() {
        const sentinel = document.getElementById('scroll-sentinel');

        if (observer) observer.disconnect();

        observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) {

                if (visibleCount < lines.length) {
                    visibleCount += increment;
                    renderTable();
                }

            }
        });

        observer.observe(sentinel);
    }



});