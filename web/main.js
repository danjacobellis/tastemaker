$(function() {
    $("#submit").on("click", function() {
        $.ajax({
            url: '/infer',
            type: 'POST',
            data: new FormData($("#form")),
            processData: false,
            contentType: false
        })
    })
})
