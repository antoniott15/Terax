$(function(){
    var url1 = "http://localhost:5000/users_profesores";

    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url1,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
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
