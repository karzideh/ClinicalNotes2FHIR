import pandas as pd
import re
import os
import warnings

import FHIRHelper
import fhirclient.models.condition as c

warnings.filterwarnings('ignore')

# annotation data from i2b2 obesity dataset
test_data = pd.read_excel(
    r'dataset\Patient_Records_Test_Mappe_Merged.xlsx')

df_test = pd.DataFrame(test_data)
df_test['fhir_info'] = ""

# fhir server with patient data
smart = FHIRHelper.createFHIRClient()
path = "dataset/cTakes/patients/test/"
for filename in os.listdir(path):
    patientId = re.findall("[0-9]+", filename)[0]
    search = c.Condition.where(struct={'_count': '1000', 'subject': 'FID'+patientId})
    condition = search.perform_resources(smart.server)
    for index, row in df_test.loc[df_test['id'] == int(patientId)].iterrows():
        for con in condition:
            df_test['fhir_info'][index] = df_test['fhir_info'][index] + str(con.as_json()) + "\n"
df_test.to_csv(r"dataset/test_with_fhir.csv", encoding='utf-8', index=False)