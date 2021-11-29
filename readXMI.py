import ctakes_parser as parser
import numpy as np
from fhir.resources.coding import Coding
from fhir.resources.condition import Condition
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.fhirtypes import IdentifierType
from fhir.resources.identifier import Identifier

df = parser.ctakes_parser.parse_file(file_path='dataset/cTakes/obesity/annotationen/obesity_sample.txt.xmi')
print(df.to_string())
print("")

conditionList = list()
# filter out every semantic element except for disease-mentions and group by cui for unique results
for disease in df[df["textsem"] == "DiseaseDisorderMention"].groupby("cui"):
    # check if disease is negated in every occurrence and if one of the occurrences is connected to the patient
    if (np.invert(disease[1]['negated']).any()) & (np.any(disease[1]['subject'] == 'patient')):
        # ToDo: add bodySite, subject
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
        print(condition)
        print("")
        conditionList.append(condition)
    # ToDo: figure out what to do whith FamiliyMember-data and with negated semantics
    else:
        print("")
        print("Negated Disease:")
        print(disease[1])
