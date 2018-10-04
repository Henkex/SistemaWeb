// Funciones públicas que pueden ser llamadas----------------------------------------------------------------------------------------------------------------------------
// Controles de los formularios en modales

function abrir_modal(url)
{
        $('#popup').load(url, function()
        {
                $(this).modal('show');
        });
        return false;
}

function cerrar_modal()
{
    $('#popup').modal('hide');
    return false;
}



//Funciones que se leen despues de contruirse el documento-------------------------------------------------------------------------------------------------------------------
$(document).ready(function(){
    // Configurando e inicializando el plugin Chosen Selects
    $(".chosen-select").chosen({no_results_text: "No se encontró coincidencias con :",
                                width: '100%' });
    
    // controles del sidebar
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

    // // Select Dinamicos Stock
    // $(".control-almacen").change(function() {
    //     // Obteniendo el ID del almácen de donde se consulta su stock de productos

    //     almacen=$(".control-almacen").val();
    //     // Creando y llenando el array de los productos obtenidos del stock
    //     const productos=[$(this).val()];
    //     data = $(this).val()
    //     if (almacen>0)
    //     {
    //         $(".control-producto").attr('disabled', false);
    //         // $.ajax({
    //         //     url:"almacen/operaciones/getproducto/",
    //         //     type: "POST",
    //         //     data: data,
    //         //     dataType: "json",
    //         //     async: true,
    //         //     success: function(j){
    //         //         var opciones = '<option value="0"> Seleccione el producto</option>';
    //         //         for (let i=0; i<j.length; i++){
    //         //             opciones += '<option value="'+parseInt(j[i].id_producto)+'">'+j[i].nombre+'</option>';
    //         //         }
    //         //         $(".control-producto").html(opciones);
    //         //     } 
    //         // })
    //     }
    //     else
    //     {
    //         $(".control-producto").attr('disabled', true);
    //     }

    // });

    // Select dinamicos de productos y su stock
    $(".control-producto").change(function(){
        var r = /\d+/;
        var s = $(this).attr("id");
        num = s.match(r);
        almacen = $(".control-almacen").val();
        nextid = "#id_formset-" + num + "-dm_cant_solicitada";
        stock  = "#id_formset-" + num + "-stock_disponible";
        $.ajax({
            url: "/almacen/operaciones/getstock/" + $(this).val()+ "/",
            type: "GET",
            dataType: "json",
            async: true,
            success: function (j) {
                //alert(nextid);
                for (let i = 0; i < j.length; i++) {
                    $(nextid).attr("max", j[i].max_value);
                    $(nextid).attr("placeholder",'Stock Disponible: '+j[i].max_value);
                    $(stock).attr("value", j[i].max_value);
                }
                $(nextid).attr('disabled', false);
            },
            error: function (xhr, errmsg, err) {
            $(nextid).attr('disabled', false);}
            // Solo activar para ver errores en un modal
            // error: function (xhr, errmsg, err) {
            //     alert(xhr.status + ": " + xhr.responseText);
            // }
        });
    });
    
    // Configuarción del plugin Datatables
    var datatable = {
        "oLanguage": {
            "oAria": {
                "sSortAscending": " - ordenar de forma ascendente",
                "sSortDescending": " - ordenar de forma descendente",
                "sInfoEmpty": "No hay información para mostrar",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sSearch": "Buscar :",
                "sZeroRecords": "No hay ningún registro",
            },
            "oPaginate": {
                "sFirst": "Primera página",
                "sLast": "Última página",
                "sNext": "Página siguiente",
                "sPrevious": "Página anterior"
            },
            "sEmptyTable": "Esta tabla no tiene datos",
            "sInfo": "Mostrando  _START_ - _END_ de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando 0 entradas",
            "sInfoFiltered": "(filtrados de _MAX_  registros en total)",
            "sLengthMenu": "Motrar _MENU_ registros",
            "sSearch": "Buscar :",
            "sZeroRecords": "No se encontraron coincidencias"
        }
    };
    var datatableresponsive = datatable;
    datatableresponsive.responsive = true;
    $('#datatable-responsive').DataTable(datatableresponsive);



})