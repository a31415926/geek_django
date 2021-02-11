function basket(actions, id){
    $.ajax({
        type : "POST",
        url : '',
        data : {
            'csrfmiddlewaretoken': window.myApp.scrf,
            'id':id,
            'action':actions,
            'qty':document.getElementById('edit_cnt_'+id).value,
        }, 
        dataType: 'json',
        cache: false, 
        success: function(data){
            if (data){
                if (data.del){
                    document.getElementById('entry_'+data.del).remove()
                }
                else{
                    console.log(data);
                    document.getElementById("cnt_"+data.id).textContent=data.qty;
                }
            }
            else{
    
            }
        }
    });}