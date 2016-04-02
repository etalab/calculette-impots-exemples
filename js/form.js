$(function(){
    var submittedForm = null;
    var inputValues = {V_ANREV:2014};
    $('#declaration-impot').submit(function(event){
        event.preventDefault();
        submittedForm = $('#declaration-impot').serializeArray();

        for(index in submittedForm){
            var element = submittedForm[index];
            inputValues[element.name] = parseFloat(element.value) || 0;
        }
        console.log(compute(inputValues));
    });
});
