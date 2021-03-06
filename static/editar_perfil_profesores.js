$(function(){
    var url2 = "http://terax.herokuapp.com/editar_perfil_profesor";

    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url2,
            insertUrl: url2,
            updateUrl: url2,
            deleteUrl: url2,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        editing: {
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },
        remoteOperations: {
            sorting: true,
            paging: true
        },
        paging: {
            pageSize: 12
        },
        pager: {
            showPageSizeSelector: true,
            allowedPageSizes: [8, 12, 20]
        },
        columns: [{
            dataField: "username"
        }, {
            dataField: "email"
        },{
            dataField: "materias"
        },{
            dataField: "telf"
        },{
            dataField: "grado"
        },{
            dataField: "institucion"
        }],
    }).dxDataGrid("instance");
});
