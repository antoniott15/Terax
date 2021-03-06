$(function(){
    var url2 = "http://terax.herokuapp.com/users_profesores";


    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url2 ,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        paging: {
            pageSize: 12
        },
        pager: {
            showPageSizeSelector: true,
            allowedPageSizes: [8, 12, 20]
        },
        columns: [{
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
