$(function(){
    $('.show_ul').click(function(){
        var url = $(this).next();
        if(url.is(':hidden')){
           
            url.show();
        }else{
            
            url.hide();
        }
    })
});