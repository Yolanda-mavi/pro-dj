

document.addEventListener('DOMContentLoaded', () => {
    const table = new DataTable('#datatableid', {
        responsive: true,
        autoWidth: true,
        destroy: true,
        deferRender: true,//solo para mas de 50000
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            // data: {
            //     action: 'searchdata'
            // },
            data: function () {
                return JSON.stringify({ action: 'searchdata' });
            },
            dataSrc: "",

            },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "name"}
        ],
        columnDefs: [{
            targets: [2],
            className: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons =' <a href="/base/product/edit/' + row.id + '/" class="btn btn-secondary btn-sm"  >  Editar </a> ';
                buttons +=' <a href="/base/product/delete/' + row.id + '/" class="btn btn-secondary btn-sm"  > Elim </a>';
                return buttons;
            }
        }],

        // complete: function (settings,json){
        //        console.log("Hola termino");
        // }

    });

});