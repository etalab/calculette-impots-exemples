$(function(){
    var submittedForm = null;
    var inputValues = {V_ANREV:2014};
    $('#declaration-impot').submit(function(event){
        event.preventDefault();
        submittedForm = $('#declaration-impot').serializeArray();

        console.dir(submittedForm);

        for(element in submittedForm){
            log(element);
            inputValues[element.name] = parseFloat(element.value);
        }
        console.log(compute(inputValues));

    });
});
