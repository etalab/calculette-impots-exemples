$(function(){
    var submittedForm = null;
    $('#declaration-impot').submit(function(event){
        submittedForm = $('#declaration-impot').serializeArray();
        event.preventDefault();
    });
});
