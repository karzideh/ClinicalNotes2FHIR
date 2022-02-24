import os
import pandas as pd
import numpy as np
import warnings

import FHIRHelper

warnings.filterwarnings('ignore')
smart = FHIRHelper.createFHIRClient()
path = "dataset/cTakes/patients/test/"

for filename in os.listdir(path):
    # create FHIR patient
    patient = FHIRHelper.createPatient(filename)
    patientId = patient.identifier[0].value
    patient.update(smart.server)
    # create Reference to patient
    reference = FHIRHelper.createReference(patient)
    df = pd.read_csv(path + filename)
    documentId = next(iter(df['true_text'][df['textsem'] == 'NumToken']), None)
    # filter out every semantic element except for disease-mentions and group by cui for unique results
    for disease in df[df["textsem"] == "SignSymptomMention"].groupby("id"):
        if (np.any(disease[1]['subject'] == 'patient')):
            condition = FHIRHelper.createCondition(disease[1], reference)
            condition.update(smart.server)
            condition