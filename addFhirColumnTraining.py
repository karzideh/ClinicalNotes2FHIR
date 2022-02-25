import pandas as pd
import re
import os
import warnings

import FHIRHelper
import fhirclient.models.condition as c
import fhirclient.models.procedure as pr
import fhirclient.models.medicationstatement as ms

warnings.filterwarnings('ignore')

# annotation data from i2b2 obesity dataset
training_data = pd.read_excel(
    r'path_to_obesity_dataset_training.xlsx')

df_train = pd.DataFrame(training_data)
# add new column to df with fhir information
df_train['fhir_info'] = ""

# fhir server with patient data
smart = FHIRHelper.createFHIRClient()
path = "dataset/cTakes/patients/training/"
for filename in os.listdir(path):
    patientId = re.findall("[0-9]+", filename)[0]
    search = c.Condition.where(struct={'_count': '2000', 'subject': 'FID'+patientId})
    condition = search.perform_resources(smart.server)
    searchProc = pr.Procedure.where(struct={'_count': '2000', 'subject': 'FID'+patientId})
    procedure = searchProc.perform_resources(smart.server)
    searchMed = ms.MedicationStatement.where(struct={'_count': '5000', 'subject': 'FID'+patientId})
    medication = searchMed.perform_resources(smart.server)
    for index, row in df_train.loc[df_train['id'] == int(patientId)].iterrows():
        for con in condition:
            df_train['fhir_info'][index] = df_train['fhir_info'][index] + str(con.as_json()) + "\n"
        for pro in procedure:
            df_train['fhir_info'][index] = df_train['fhir_info'][index] + str(pro.as_json()) + "\n"
        for med in medication:
            df_train['fhir_info'][index] = df_train['fhir_info'][index] + str(med.as_json()) + "\n"
df_train.to_csv(r"dataset/training_data.csv", encoding='utf-8', index=False)