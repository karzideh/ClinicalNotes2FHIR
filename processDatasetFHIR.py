import os
import pandas as pd
import numpy as np
from fhirclient import client

import FHIRHelper as fhirhelper

settings = {
    'app_id': 'hapi-fhir',
    'api_base': 'http://localhost:8080/fhir/'
}

smart = client.FHIRClient(settings=settings)
path = "dataset/cTakes/patients/training/"
for filename in os.listdir(path):
    # create FHIR patient
    patient = fhirhelper.createPatient(filename)
    patient.update(smart.server)
    # create Reference to patient
    reference = fhirhelper.createReference(patient)
    df = pd.read_csv(path + filename)
    documentId = next(iter(df['true_text'][df['textsem'] == 'NumToken']), None)
    print(df.to_string())
    # filter out every semantic element except for disease-mentions and group by cui for unique results
    for disease in df[df["textsem"] == "DiseaseDisorderMention"].groupby("id"):
        #print(disease[1].to_string())
        # check if disease is negated in every occurrence and if one of the occurrences is connected to the patient
        if (np.any(disease[1]['subject'] == 'patient')):
            condition = fhirhelper.createCondition(disease[1], reference)
            #for siteMention in df[df["textsem"] == "AnatomicalSiteMention"].groupby("cui"):
            #    if(siteMention[1]["cui"]==disease[1]["cui"]):
            condition.update(smart.server)
            condition
        """
        else:
            print("")
            print("Negated Disease:")
            print(disease[1])
            #np.invert(disease[1]['negated']).any()) &
            """
        """
        elif np.any(disease[1]['subject'] == 'family_member'):
            fm = fmh.FamilyMemberHistory()
            fm.patient = reference
            fm.status = "partial"
            fm.id = counter
            counter+= 1
            referenceFM = ref.Reference()
            referenceFM.reference = "FamiliyMemberHistory/" + fm.id
            referenceFM.resource_type = fm.resource_type
            condition = c.Condition()
            codeableConcept = cc.CodeableConcept()
            codingListFM = list()
            for code in disease[1].groupby("code"):
                coding = cdg.Coding()
                coding.code = code[0]
                coding.display = disease[1]['preferred_text'].values[0]
                coding.system = "http://snomed.info/sct"
                codingListFM.append(coding)
            codeableConcept.coding = codingList
            condition.code = codeableConcept
            condition.subject =
            """
