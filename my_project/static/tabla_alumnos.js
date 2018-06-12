$(function(){
    var url2 = "http://localhost:5000/users_alumnos";


    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url2 ,
            insertUrl: url2 ,
            updateUrl: url2 ,
            deleteUrl: url2 ,
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
        }, {
            dataField: "username_alumno"
        }, {
            dataField: "password"
        }, {
            dataField: "email_alumno"
        },{
            dataField: "grado"
        },{
            dataField: "direccion"
        },{
            dataField: "edad"
        },{
            dataField: "institucion"
        }],
    }).dxDataGrid("instance");
});
