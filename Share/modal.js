var element;
$( document ).ready(function() {

    $("map").on("click", "area",function(e){
        e.preventDefault()
        element = e.target
        jQuery('#tooltip-modal').modal()
    })  

    $('#tooltip-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) 
        var modal = $(this)
        var html = $(element).attr("tooltip")
        modal.find('.modal-body').html(html)

        var container = modal.find('#thumbnail')
        $(container).css("width", 450)
        var img = modal.find('#thumbnail>img')
        $(img).attr("width", 450)
        var link = $("<a/>")
        $(link).attr("href", element.href)
        $(link).attr("target", "_blank")
        $(img).wrap(link)
      })
});