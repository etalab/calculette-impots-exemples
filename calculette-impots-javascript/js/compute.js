// Logger helper
function log(something,choice){
  if(typeof(choice)==='undefined'){
    return console.log(something);
  }else if(choice === 1 ){
    return console.error(something);
  }else if(choice === 2){
    return console.warn(something);
  }else{
    return console.log(something);
  }
};

var constants = null;
var formulas = null;
var computingOrder = null;

// Get Abstract syntax tree
$.getJSON('json/constants_light.json',function(response){
   constants = response;
   return ;
});

$.getJSON('json/formulas_light.json',function(response){
   formulas = response;
   return ;
});

$.getJSON('json/computing_order.json',function(response){
   computingOrder = response;
   return ;
});



// Computations rules
var functionsMapping = {

    '+':function sumTab(tabValeurs){
         return tabValeurs.reduce(function(a,b){
            return a+b;
        });
    },

    '*':function mulTab(tabValeurs){
        return tabValeurs.reduce(function(a,b){
            return a*b;
        });
    },

    '-':function negateTab(tabValeurs){
        return -tabValeurs[0];
    },

    'unary:-':function negateTab(tabValeurs){
        return -tabValeurs[0];
    },

    'positif': function positifTab(tabValeurs){
        return (tabValeurs[0]>0) | 0;
    },

    'positif_ou_nul': function positifOuNulTab(tabValeurs){
        return (tabValeurs[0]>=0) | 0;
    },

    'null': function nullTab(tabValeurs){
        return (tabValeurs[0] === 0) | 0;
    },

    'operator:>': function supTab(tabValeurs){
        return (tabValeurs[0] > tabValeurs[1] ) | 0;
    },

    'operator:>=': function supOuEgalTab(tabValeurs){
        return (tabValeurs[0] >= tabValeurs[1] ) | 0;
    },

    'operator:=': function operatorEgalTab(tabValeurs){
        return (tabValeurs[0] === tabValeurs[1] ) | 0;
    },

    'operator:<': function infTab(tabValeurs){
        return (tabValeurs[0] < tabValeurs[1] ) | 0;
    },

    'ternary': function ternaryTab(tabValeurs){
        return (tabValeurs[0] ? tabValeurs[1] : tabValeurs[2] );
    },

    'si': function siTab(tabValeurs){
        return (tabValeurs[0] ? tabValeurs[1] : 0 );
    },

    'inverse': function inverseTab(tabValeurs){
        return (tabValeurs[0] !== 0 ? 1/tabValeurs[0] : 0 );
    },

    'max': function maxTab(tabValeurs){
        return tabValeurs.reduce(function(a,b){
            return Math.max(a,b);
        });
    },

    'min': function minTab(tabValeurs){
        return tabValeurs.reduce(function(a,b){
            return Math.min(a,b);
        });
    },

    'inf': function infTab(tabValeurs){
        return Math.floor(tabValeurs[0]);
    },

    'arr': function arrTab(tabValeurs){
        return Math.round(tabValeurs[0]);
    },

    'abs': function absTab(tabValeurs){
        return Math.abs(tabValeurs[0]);
    },

    'present': function presentTab(tabValeurs){
        return (tabValeurs[0] !== 0);
    },

    'boolean:ou': function ouTab(tabValeurs){
        return tabValeurs.reduce(function(a,b){
           return (a || b) | 0;
        });
    },

    'boolean:et': function etTab(tabValeurs){
        return tabValeurs.reduce(function(a,b){
           return (a && b) | 0;
        });
    },

    'dans': function dansTab(tabValeurs){

        for(var i=1; i< tabValeurs.length; i++ ){
            if(tabValeurs[0] === tabValeurs[i]){
                return 1;
            }
        };
        return 0;
    }

};

// Computation
function compute(inputValues){
  var values = {};

  for(item in constants){
    values[item] = constants[item];
  }

  for(item in inputValues){
    values[item]= inputValues[item];
  }

  for(i in computingOrder){
    var name = computingOrder[i];
    formula = formulas[name];
    var value = computeFormula(formula,values);
    values[name] = value;
  }

  return values;

 }

 // Apply computation formulas
function computeFormula(node, values){

    if(node.nodetype ==='symbol'){
        var value = values[node.name];
        if(typeof(value)==='undefined'){
            value = 0;
        };
        return value

    }else if(node.nodetype ==='float'){

        return node.value;

    }else if(node.nodetype==='call'){
        var name = node.name;
        var func = functionsMapping[name];
        var args = [];
        for(i in node.args){
           args.push(computeFormula(node.args[i],values));
        }
        return func(args);
    }
}
