var element;
$( document ).ready(function() {
    var modal = ''.concat(
        '<div class="modal fade" id="tooltip-modal" tabindex="-1" role="dialog" aria-hidden="true">',
        '<div class="modal-dialog modal-lg" role="document">',
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
    
    $("#modal-content").on("click", ".btn.model.decrement",function(e){
        console.log("model.decrement")
        var el = document.getElementById(element.dataset.modelleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.model.increment",function(e){
        console.log("model.increment")
        var el = document.getElementById(element.dataset.modelright)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.variable.decrement",function(e){
        console.log("variable.decrement")
        var el = document.getElementById(element.dataset.variableleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.variable.increment",function(e){
        console.log("variable.increment")
        var el = document.getElementById(element.dataset.variableright)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.season.decrement",function(e){
        console.log("season.decrement")
        var el = document.getElementById(element.dataset.seasonleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.season.increment",function(e){
        console.log("season.increment")
        var el = document.getElementById(element.dataset.seasonright)
        if(el){
            element = el
            populateModal()
        }
    })

    $('#tooltip-modal').on('show.bs.modal', function (event) {
        populateModal()
    })
});

function populateModal(){
    var container = $('#modal-content')
    var content = getContent(element)
    container.empty()
    container.append(content)
}

function getContent(el){
    var new_elements = []
    var prev_disabled;
    var next_disabled;

    prev_disabled = el.dataset["modelleft"] ? "" : "disabled"
    next_disabled = el.dataset["modelright"] ? "" : "disabled"
    new_elements.push(
        $("".concat(
            "<div id=current-model>",
                "<button type='button' class='btn btn-outline-info btn-sm model decrement' style='line-height: 5px'", prev_disabled,"> &lsaquo; </button>",
                "<button type='button' class='btn btn-outline-info btn-sm model increment' style='line-height: 5px'", next_disabled,"> &rsaquo; </button>",
                "<span class='field-label' style='margin-left: 4px;'>Model: </span>",
                "<span class='field-value'>",
                el.dataset["model"],
                " </span>",
            "</div>"
        ))
    )

    prev_disabled = el.dataset["variableleft"] ? "" : "disabled"
    next_disabled = el.dataset["variableright"] ? "" : "disabled"
    new_elements.push(
        $("".concat(
            "<div id=current-variable>",
                "<button type='button' class='btn btn-outline-info btn-sm variable decrement' style='line-height: 5px'", prev_disabled,"> &lsaquo; </button>",
                "<button type='button' class='btn btn-outline-info btn-sm variable increment' style='line-height: 5px'", next_disabled,"> &rsaquo; </button>",
                "<span class='field-label' style='margin-left: 4px;'>Variable: </span>",
                "<span class='field-value'>",
                el.dataset["variable"],
                " </span>",
            "</div>"
        ))
    )

    if(element.dataset["Season"]){
        prev_disabled = el.dataset["seasonleft"] ? "" : "disabled"
        next_disabled = el.dataset["seasonright"] ? "" : "disabled"
        new_elements.push(
            $("".concat(
                "<div id=current-season>",
                    "<button type='button' class='btn btn-outline-info btn-sm season decrement' style='line-height: 5px'", next_disabled,"> &lsaquo; </button>",
                    "<button type='button' class='btn btn-outline-info btn-sm season increment' style='line-height: 5px'", next_disabled,"> &rsaquo; </button>",
                    "<span class='field-label' style='margin-left: 4px;'>Season: </span>",
                    "<span class='field-value'>",
                    el.dataset["Season"],
                    " </span>",
                "</div>"
            ))
        )
    }

    new_elements.push(
        $("".concat(
            "<div id=current-value>",
                "<button type='button' class='btn btn-outline-secondary btn-sm' style='visibility:hidden;' disabled> &lsaquo; </button>",
                "<button type='button' class='btn btn-outline-secondary btn-sm' style='visibility:hidden;' disabled> &rsaquo; </button>",
                "<span class='field-label' style='margin-left: 4px;'>Value: </span>",
                "<span class='field-value'>",
                el.dataset["value"],
                " </span>",
            "</div>"
        ))
    )

    new_elements.push(
        $("".concat("<img class='full-image' style='margin: 0 auto; width: 100%; max-height: calc(100% - 300px);' src='", el.dataset["image"], "'>"))
    )
    return new_elements
}
