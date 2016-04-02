import numpy as np
import os

def gen(n):

    cases = []

    rv = np.random.rand(n,12)

    for i in range(0,n):

        case = {}

        # Repartition marié/célib... (40% celib 0AC, 32% marié 0AM, 15% divorcés 0AD, 8% veufs 0AV, 5% pacsés 0AO)
        # bool, sum == 1

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

        # Enfants à charge mineurs ou handicapés : 0CF (int) 27% moyenne: 1.8
        # note: besoin date naissance?

        if (rv[i,2] < 0.27):
            case['0CF'] = int(np.round(echantillonnage(1.8)))

        # Enfants majeurs ou mariés: 0DJ (int) 5% moyenne: 1

        if (rv[i,3] < 0.05):
            case['0CF'] = int(np.round(echantillonnage(1)))

        # Déclarants (fonction situation maritale)
        # salaires : 1AJ, 1BJ 57% moyenne: 24000, 20300
        # autres revenus : 1AP, 1BP 11% moyenne: 6186, 6100
        # pensions retraites 1AS, 1BS 31%  moyenne : 19682, 12188

        if (rv[i,4] < 0.57):
            case['1AJ'] = int(echantillonnage(24000))
        elif (rv[i,4] < 0.62):
            case['1AP'] = int(echantillonnage(6186))
        elif (rv[i,4] < 0.93):
            case['1AS'] = int(echantillonnage(19682))

        if (('0AM' in case) | ('0AO' in case)):
            if (rv[i,5] < 0.57):
                case['1BJ'] = int(echantillonnage(20300))
            elif (rv[i,5] < 0.62):
                case['1BP'] = int(echantillonnage(6100))
            elif (rv[i,5] < 0.93):
                case['1BS'] = int(echantillonnage(12188))

        # Abattements
        # revenus action et parts 2DC 27% moy : 1400

        if (rv[i,6] < 0.27):
            case['2DC'] = int(echantillonnage(1400))

        # interet placements revenus fixes 2TR 30% moy : 652

        if (rv[i,7]  < 0.3):
            case['2TR'] = int(echantillonnage(652))

        # credit d'impot egal au prelevement forfaitaire non obligatoire en 2014 2CK 30% moy : 324

        if (rv[i,8] < 0.3):
            case['2CK'] = int(echantillonnage(324))

        # Revenus fonciers imposables 4BA 7% moy : 12500

        if (rv[i,9] < 0.07):
            case['4BA'] = int(echantillonnage(12500))

        # CSG déductible 6DE 11% moy: 717

        if (rv[i,10] < 0.11):
            case['6DE'] = int(echantillonnage(717))

        # Dons versés à des associations 7UF 13% 450

        if (rv[i,11] < 0.13):
            case['7UF'] = int(echantillonnage(450))

        cases.append(case)

    return cases

def echantillonnage(value):
    ### Several statistics dirtributions possible
    #return np.random.randint(0, 2*value)
    #return np.absolute(np.random.normal(value, value/2))
    return np.round(np.random.chisquare(value))
