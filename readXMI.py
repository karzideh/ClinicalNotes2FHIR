import ctakes_parser as parser
from fhir.resources.coding import Coding
from fhir.resources.condition import Condition
from fhir.resources.codeableconcept import CodeableConcept

df = parser.ctakes_parser.parse_file(file_path='dataset/cTakes/obesity/annotationen/obesity_sample.txt.xmi')
print(df.to_string())
print("")
for disease in df[df["textsem"] == "DiseaseDisorderMention"].groupby("cui"):
    if disease[1]['negated'] is not True:
        condition = Condition.construct()
        cc = CodeableConcept.construct()
        cc.coding = list()
        for code in disease[1].groupby("code"):
            coding = Coding.construct()
            #coding.code = disease[1]['code'].values[0]
            coding.code = code[0]
            coding.display = disease[1]['preferred_text'].values[0]
            coding.system = "http://snomed.info/sct"
            cc.coding.append(coding)
        condition.code = cc
        print(condition)
        print("")
    else:
        print("")
        print("Negated Disease:")
        print(disease[1])
