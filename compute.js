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
    }

    '-':function negateTab(tabValeurs){
        return -tabValeurs[0];
    },

    'positif': function positifTab(tabValeurs){
        return (tabValeurs[0]>0) | 0;
    },

    'positif_ou_nul': function positifOuNulTab(tabValeurs){
        return (tabValeurs[0]<0) | 0;
    },

    'null': function nullTab(tabValeurs){
        return (tabValeurs[0] === 0) | 0;
    },

    'operator:>=': function supOuEgalTab(tabValeurs){
        return (tabValeurs[0] >= tabValeurs[1] ) | 0;
    },

    'operator:=': function operatorEgalTab(tabValeurs){
        return (tabValeurs[0] === tabValeurs[1] ) | 0;
    },

    'ternary': function ternaryTab(tabValeurs){
        return (tabValeurs[0] ? tabValeurs[1] : tabValeurs[2] );
    },

    'si': function siTab(tabValeurs){
        return (tabValeurs[0] ? tabValeurs[1] : 0 );
    },

    'inverse': function inverseTab(tabValeurs){
        return (tabValeurs[0] !== 0 ? 1/tabValeurs[0] : 0 );
    }


};
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
        for(child in node.args){
           args.push(computeFormula(child,values));
        }
        return func(args);
    }
}
