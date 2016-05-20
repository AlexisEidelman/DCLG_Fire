# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 11:40:01 2016

@author: Alexis
"""

import os
import pandas as pd

path = "~/data/BSPP"


tab = pd.read_csv(os.path.join(path, "Intervention.csv"),
                  encoding='cp1252', sep=';')

# remove useless columns
to_remove = [u'ID207 Date De Début D intervention',
             u'ID208 Heure De Début D intervention',
             'ID209 Date Fin Intervention',
             'ID210 Heure De Fin D intervention',
             'Abrege Motif Alerte',
             'Compte Rendu Intervention 218 Code CRI',
             'Libelle Adresse Reel',
             'Numero Dans La Voie',
             'Type De Voie',
             'Libelle Voie',
             'Code Commune', 'Libelle Commune',
             'Numero Departement', 'Libelle Departement',
             'ID202 Numéro Intervention'
             ]
tab1 = tab[[x for x in tab.columns if x not in to_remove]]

# Comparaison avec le fichier de test
# les séparateurs sont des ','



#  <- 
rename = {'Numero Iris': "DCOMIRIS",
          u'Libelle Iris': "NOM_IRIS",


          }
tab1.rename(columns = rename, inplace=True)

tab1.sort_values([u'GDH début'], inplace=True)

path_DCLG = '~/git/DCLG_Fire/static/data'
tab1.dropna(inplace=True)
tab1.to_csv(os.path.join(path_DCLG, 'BSPP_TEST.csv'),
            encoding='utf8',
            index=False,
            sep=',')

## Tentative suivante : transformer au plus proche possible du fichier anglais
tab2 = tab1.copy()
tab2['DateOfCall'] = tab1[u'GDH début'].str[:10] # change format DateOfCall
tab2['TimeOfCall'] = tab1[u'GDH début'].str[11:19]

rename2 = {u'Motif De Départ 212 Motif De L alerte': "StopCodeDescription",
          u'ID206 CSTC': "PropertyCategory", # fake mais passons
          u'Code Postal': 'Postcode_district',
          u'NOM_IRIS':'WardName',
          u'Total 329 Délai Présentation Des Premiers Intervenants':'FirstPumpArriving_AttendanceTime', 
          }
tab2.rename(columns = rename2, inplace=True)
tab2['Postcode_district'] = tab2['Postcode_district'].astype(int)
tab2['FirstPumpArriving_AttendanceTime'] = tab2['FirstPumpArriving_AttendanceTime'].astype(int)
tab2.to_csv(os.path.join(path_DCLG, 'BSPP_TEST2.csv'),
            encoding='utf8',
            index=False,
            sep=',')




