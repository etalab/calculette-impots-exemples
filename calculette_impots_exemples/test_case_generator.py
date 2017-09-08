import numpy as np
import os
import scipy.stats

def gen(n):

    cases = []

    rv = np.random.rand(n,12)

    for i in range(0,n):

        case = {}

        # Repartition marié/célib... (40% celib 0AC, 32% marié 0AM, 15% divorcés 0AD, 8% veufs 0AV, 5% pacsés 0AO)
        # boolean

        if (rv[i,1] < 0.4):
            case['0AC'] = 1
        elif (rv[i,1] <0.72):
            case['0AM'] = 1
        elif (rv[i,1] <0.87):
            case['0AD'] = 1
        elif (rv[i,1] <0.95):
            case['0AV'] = 1
        else:
            case['0AO'] = 1

        # Enfants à charge mineurs ou handicapés : 0CF (int), 27% des cas, moyenne: 1.8
        # note: besoin date naissance?

        if (rv[i,2] < 0.27):
            case['0CF'] = int(np.round(tirage(1.8)))

        # Enfants majeurs ou mariés: 0DJ (int), 5% des cas, moyenne: 1

        if (rv[i,3] < 0.05):
            case['0DJ'] = int(np.round(tirage(1)))

        # Déclarants (fonction situation maritale)
        # salaires : 1AJ, 1BJ, 57% des cas, moyenne: 24000, 20300
        # autres revenus : 1AP, 1BP, 11% des cas, moyenne: 6186, 6100
        # pensions retraites 1AS, 1BS, 31% des cas, moyenne : 19682, 12188

        if (rv[i,4] < 0.57):
            case['1AJ'] = int(tirage(24000))
        elif (rv[i,4] < 0.62):
            case['1AP'] = int(tirage(6186))
        elif (rv[i,4] < 0.93):
            case['1AS'] = int(tirage(19682))

        if (('0AM' in case) | ('0AO' in case)):
            if (rv[i,5] < 0.57):
                case['1BJ'] = int(tirage(20300))
            elif (rv[i,5] < 0.62):
                case['1BP'] = int(tirage(6100))
            elif (rv[i,5] < 0.93):
                case['1BS'] = int(tirage(12188))

        # Abattements
        # revenus action et parts 2DC, 27% des cas, moyenne : 1400

        if (rv[i,6] < 0.27):
            case['2DC'] = int(tirage(1400))

        # interet placements revenus fixes 2TR, 30% des cas, moyenne : 652

        if (rv[i,7]  < 0.3):
            case['2TR'] = int(tirage(652))

        # credit d'impot egal au prelevement forfaitaire non obligatoire en 2014 2CK, 30% des cas, moyenne : 324

        if (rv[i,8] < 0.3):
            case['2CK'] = int(tirage(324))

        # Revenus fonciers imposables 4BA, 7% des cas, moyenne : 12500

        if (rv[i,9] < 0.07):
            case['4BA'] = int(tirage(12500))

        # CSG déductible 6DE, 11% des cas, moyenne : 717

        if (rv[i,10] < 0.11):
            case['6DE'] = int(tirage(717))

        # Dons versés à des associations 7UF, 13% des cas, moyenne : 450

        if (rv[i,11] < 0.13):
            case['7UF'] = int(tirage(450))

        cases.append(case)

    return cases

def tirage(value):
    ### Several statistics dirtributions possible
    # Fonction random entre 0 et 2*value
    # return np.random.randint(0, 2*value)
    # Fontion random suivant une loi normale en prenant la valeur absolue
    # return np.absolute(np.random.normal(value, value/2))

    # Fonction random suivant une loi de Fisk
    return np.round(scipy.stats.fisk.rvs(4, loc=0, scale=value))
