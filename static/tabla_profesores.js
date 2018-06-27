$(function(){
    var url1 = "http://terax.herokuapp.com/users_profesores";

    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
             loadUrl: url1 ,
             insertUrl: url1 ,
             updateUrl: url1 ,
             deleteUrl: url1 ,
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
            dataField: "id",
            dataType: "number",
            allowEditing: true
        },{
            dataField: "username"
        },{
            dataField: "password"
        },{
            dataField: "texto"
        },{
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
