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
        var values = compute(inputValues);
        if (values.NAPT >= 0) {
          $('#resultat').html('<h4>Somme à restituer: '+values.IREST+'</h4>');
        }
        else {
          $('#resultat').html('<h4>Votre impot: '+values.IRN+'</h4>');
        }
    });
});
