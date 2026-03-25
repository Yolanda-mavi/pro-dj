// function message_error(obj){
//     var html = "<ul style='text-align: left;'>"
//
//     Object.entries(obj).forEach(([key, value]) => {
//         html +="<li>"+key+":"+ value+"</li> "
//       //console.log(`${clave}: ${valor}`);
//     });
//     html +="</ul>"
//      alert(html);
// }
// function message_error(errors) {
//     let message = '';
//
//     if (typeof errors === 'object') {
//         for (const [key, value] of Object.entries(errors)) {
//             message += `${key}: ${value}\n`;
//         }
//     } else {
//         message = errors;
//     }
//
//     alert(message);
// }

// function message_error(errors) {
//     const container = document.getElementById('errorContainer');
//     container.innerHTML = ''; // limpiar errores previos
//
//     let html = '<div class="alert alert-danger">';
//
//     if (typeof errors === 'object') {
//         html += '<ul>';
//         for (const [key, value] of Object.entries(errors)) {
//             html += `<li><strong>${key}:</strong> ${value}</li>`;
//         }
//         html += '</ul>';
//     } else {
//         html += `<p>${errors}</p>`;
//     }
//
//     html += '</div>';
//
//     container.innerHTML = html;
// }

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

    // eliminar después de ocultarse
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
// function show_errors_toast(errors) {
//     if (typeof errors === 'object') {
//         for (const [field, messages] of Object.entries(errors)) {
//             messages.forEach(msg => {
//                 show_toast(`${field}: ${msg}`, 'danger');
//             });
//         }
//     } else {
//         show_toast(errors, 'danger');
//     }
// }
// function show_field_errors(errors) {
//
//     // limpiar errores previos
//     document.querySelectorAll('.is-invalid').forEach(el => {
//         el.classList.remove('is-invalid');
//     });
//
//     document.querySelectorAll('.invalid-feedback').forEach(el => {
//         el.innerHTML = '';
//     });
//
//     // recorrer errores
//     for (const [field, messages] of Object.entries(errors)) {
//         const input = document.querySelector(`[name="${field}"]`);
//
//         if (input) {
//             input.classList.add('is-invalid');
//
//             const feedback = input.closest('.form-group')
//                                   .querySelector('.invalid-feedback');
//
//             if (feedback) {
//                 feedback.innerHTML = messages.join('<br>');
//             }
//         }
//     }
// }
