var element;
$( document ).ready(function() {
    var modal = ''.concat(
        '<div class="modal fade" id="tooltip-modal" tabindex="-1" role="dialog" aria-hidden="true">',
        '<div class="modal-dialog" role="document">',
            '<div class="modal-content">',
            '<div class="modal-header">',
                '<h5 class="modal-title" id="tooltipModalLabel"></h5>',
                '<button type="button" class="close" data-dismiss="modal" aria-label="Close">',
                '<span aria-hidden="true">&times;</span>',
                '</button>',
            '</div>',
            '<div id="modal-content" class="modal-body">',
            '</div>',
            '<div class="modal-footer">',
                '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>',
            '</div>',
            '</div>',
        '</div>',
        '</div>'
    )
    $(document.body).append(modal)
    // We need to guarantee that the modal will exist. 
    // So we add it with javascript, rather than hoping that the user includes it in their script. 

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