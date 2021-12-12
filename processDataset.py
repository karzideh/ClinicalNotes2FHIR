import os
import re
import pandas as pd
import numpy as np
from fhir.resources import fhirtypes
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.condition import Condition
from fhir.resources.identifier import Identifier
from fhir.resources.patient import Patient
from fhir.resources.reference import Reference

path = "dataset/cTakes/patients/training/"
for filename in os.listdir(path):
    patient = Patient.construct()
    identifierList = list()
    identifier = Identifier.construct()
    patientId: fhirtypes.String = re.findall("[0-9]+", filename)[0]
    identifier.value = patientId
    identifier.system = "http://www.acme.com/identifiers/patient/i2b2obesity"
    identifierList.append(identifier)
    patient.identifier = identifierList
    df = pd.read_csv(path+filename)
    documentId = next(iter(df['true_text'][df['textsem'] == 'NumToken']), None)
    print(df.to_string())
    # filter out every semantic element except for disease-mentions and group by cui for unique results
    for disease in df[df["textsem"] == "DiseaseDisorderMention"].groupby("cui"):
        # check if disease is negated in every occurrence and if one of the occurrences is connected to the patient
        if (np.invert(disease[1]['negated']).any()) & (np.any(disease[1]['subject'] == 'patient')):
            condition = Condition.construct()
            cc = CodeableConcept.construct()
            cc.coding = list()
            for code in disease[1].groupby("code"):
                coding = Coding.construct()
                # coding.code = disease[1]['code'].values[0]
                coding.code = code[0]
                coding.display = disease[1]['preferred_text'].values[0]
                coding.system = "http://snomed.info/sct"
                cc.coding.append(coding)
            condition.code = cc
            reference = Reference.construct(patient)
            condition.subject = reference
            condition
        else:
            print("")
            print("Negated Disease:")
            print(disease[1])