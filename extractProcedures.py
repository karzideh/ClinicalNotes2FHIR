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
    # filter out every semantic element except for disease-mentions and group by cui for unique results
    for procedure in df[df["textsem"] == "ProcedureMention"].groupby("id"):
        if (np.any(procedure[1]['subject'] == 'patient')):
            proc = FHIRHelper.createProcedure(procedure[1], reference)
            proc.update(smart.server)
