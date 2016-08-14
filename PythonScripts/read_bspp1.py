# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 11:40:01 2016

@author: Alexis
"""

import os
import pandas as pd

path = 'C:/git/BSPP1/adagio'
path = '~/data/BSPP'
path_DCLG = '~/git/DCLG_Fire/static/data/'


tab = pd.read_csv(os.path.join(path, 'interventions_fin.csv'), sep=';')

# remove useless columns
to_remove = ['IdMMASelection', 'IdIntervention', 'IdMMA', 'IdAdresseIntervention',
              'TypeSelection', 'FamilleRessourcesDotation',
              'FamilleRessourcesType',
              'IdObjetGeo', 'IdAdresse', 'X', 'Y', 
              #'Cstc',
              #'LibelleAdresse',
              'IdSIG',
              'TypeAdresse', 'NbEngin', 'totalParti', 'totalPresente',
              'IdGrilleDepart', 'CodeCri', 
              #'LibelleMotifAlerte',
              #'LibelleMotifAlerteType', 'Instance départ', 'Parti', 'Sur les lieux',
              'Rentré', 'Disponible', 'hopital']

# TODO: utiliser des table pour rattraper CodeCri et 
# le transformer en Libellé Cri
          
tab1 = tab[[x for x in tab.columns if x not in to_remove]]
tab1['code_postal'] = tab1['LibelleAdresse'].str.extract('(\d{5})')
tab1['departement'] = tab1['code_postal'].str[:2]

tab1.sort_values(['Instance départ'], inplace=True)


tab1.dropna(inplace=True)

## Tentative suivante : transformer au plus proche possible du fichier anglais
tab2 = tab1.copy()
tab2['DateOfCall'] = tab1[u'Instance départ'].str[:10] # change format DateOfCall
tab2['TimeOfCall'] = tab1[u'Instance départ'].str[11:19]

rename2 = {u'Motif De Départ 212 Motif De L alerte': "StopCodeDescription",
          u'ID206 CSTC': "PropertyCategory", # fake mais passons
          # u'Code Postal': 'Postcode_district',
          #u'NOM_IRIS':'WardName',
          u'Total 329 Délai Présentation Des Premiers Intervenants':'FirstPumpArriving_AttendanceTime',
          }

tab2.rename(columns = rename2, inplace=True)
tab2[u'Code Postal'] = tab2[u'code_postal'].astype(int)
del tab2[u'code_postal']
tab2[u'Numero Departement'] = tab2[u'departement'].astype(int)
del tab2[u'departement']

timedelta_arrivee = pd.to_datetime(tab2['Sur les lieux']) - pd.to_datetime(tab2['Instance départ'])
temps_seconde_arrivee = timedelta_arrivee/pd.Timedelta('1s')
tab2['FirstPumpArriving_AttendanceTime'] = temps_seconde_arrivee.astype(int)

tab2 = tab2[[u'Code Postal',u'Numero Departement',
             'FirstPumpArriving_AttendanceTime',
             'DateOfCall', 'TimeOfCall',
             'LibelleMotifAlerte',
             'LibelleMotifAlerteType'
             ]]

tab2['NOM_IRIS'] = 'Jardin Parisien 2'
tab2['Code Commune'] = '6864581'


tab2.to_csv(os.path.join(path_DCLG, 'BSPP_TEST2.csv'),
            encoding='utf8',
            index=False,
            sep=',')
