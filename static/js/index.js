
$(function(){
    $('.request').each(function(){
        //$(this).addClass('status_active')
        //var $chng_btn = $(this).find('.chng_button a')
        //$chng_btn.attr('href', $chng_btn.attr('href') + '?type=edit&in_num=' +  $(this).find('.req_in_num').text())
        var curr_date = new Date().valueOf();
        var out_date = new Date($(this).find('.req_out_date').text().replace(/(\d+)-(\d+)-(\d+)/, '$2/$1/$3')).valueOf();
        var perehod = '2011-04-25 12:00:00';
        var test = new Date(perehod.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'))
        var out_num = $(this).find('.req_out_num').text();
        if(out_num != ''){
            $(this).addClass('status_complete')
        }
        else if(curr_date > out_date){
            $(this).addClass('status_overdue')
        }
        else{
            $(this).addClass('status_active')
        }
    })
});


