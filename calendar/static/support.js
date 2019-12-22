
    $("#cal-table td").click(function(){
        var td_now = $(this).text();
        $("#selDate").val(td_now);
    })

    $("#sample td").click(function(){
        var td_now = $(this).text();
        $("#input").val(td_now);
    })

