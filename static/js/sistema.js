// Funciones públicas que pueden ser llamadas----------------------------------------------------------------------------------------------------------------------------
// Controles de los formularios en modales

// Función que hace que el loader aparezca por un tiempo establecido
var myVar;

function myFunction() {
    myVar = setTimeout(showPage, 700);
}

function showPage() {
  document.getElementById("lds-ripple").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}
// Función que hace que el loader solo espere en cargas verdaderas
// window.onload = function(){
//     var myVar = document.getElementById("lds-ripple");
//     myVar.style.display = "none";
//     document.getElementById("myDiv").style.display = "block";
// }

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

$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-group:last', 'formset');
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('formset', $(this));
    return false;
});

//Funciones que se leen despues de contruirse el documento-------------------------------------------------------------------------------------------------------------------
$(document).ready(function(){
    // Configurando e inicializando el plugin Chosen Selects
    $(".chosen-select").chosen({no_results_text: "No se encontró coincidencias con :",
                                width: '100%' });

    // $(function() {
    //     $('form .formset').formset();
    // });
    $('.selectpicker').selectpicker();

    
    // controles del sidebar
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

    // Select dinamicos de productos y su stock
    $(".control-producto").change(function(){
        var r = /\d+/;
        var s = $(this).attr("id");
        num = s.match(r);
        nextid = "#id_formset-" + num + "-dm_cant_solicitada";
        stock  = "#id_formset-" + num + "-stock_disponible";
        if($(this).val()>0){
            $.ajax({
                url: "/almacen/operaciones/getstock/" + $(this).val()+ "/",
                type: "GET",
                dataType: "json",
                async: true,
                success: function (j) {
                    //alert(nextid);
                    for (let i = 0; i < j.length; i++) {
                        $(nextid).attr("max", j[i].max_value);
                        $(nextid).attr("placeholder",'Disponible: '+j[i].max_value);
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
        }

        else{
            $(nextid).attr("placeholder",'Stock Disponible: 0');
            $(nextid).attr('disabled', true);
        }   
        
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
    $('#datatable-responsive').DataTable(
        datatableresponsive
        );

})