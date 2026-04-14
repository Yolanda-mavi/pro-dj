/* Funciones para errores genericos  *falta mejorar en caso de error de pyton nose muestra y cuando un getlines tiene el nombre incorrecto en python y js*/
function show_toast(message, type = 'danger') {
    const container = document.getElementById('toastContainer');

    const toastHTML = `
        <div class="toast align-items-center text-bg-${type} border-0 mb-2" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = container.lastElementChild;
    const toast = new bootstrap.Toast(toastElement, { delay: 4000 });

    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function show_errors_toast(errors) {
    let messages = [];

    for (const [field, msgs] of Object.entries(errors)) {
        msgs.forEach(msg => {
            messages.push(`${field}: ${msg}`);
        });
    }

    show_toast(messages.join('<br>'), 'danger');
}



