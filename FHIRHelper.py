import re
import fhirclient.models.patient as p
import fhirclient.models.identifier as i
import fhirclient.models.fhirreference as ref
import fhirclient.models.condition as c
import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as cdg
import fhirclient.models.extension as ex
import fhirclient.models.documentreference as dr
import fhirclient.models.domainresource as dor
import fhirclient.models.quantity as qu
import fhirclient.models.range as ra
import fhirclient.models.fhirdate as fd
from pandas import DataFrame
from fhirclient import client


def createFHIRClient():
    # Settings of the setup FHIR Server
    settings = {
        'app_id': 'hapi-fhir',
        'api_base': 'http://localhost:8080/fhir/'
    }
    smart = client.FHIRClient(settings=settings)
    return smart

def createPatient(filename):
    patient = p.Patient()
    identifierList = list()
    identifier = i.Identifier()
    patientId = re.findall("[0-9]+", filename)[0]
    identifier.value = patientId
    identifier.system = "https://www.i2b2.org/NLP/Obesity/"
    identifierList.append(identifier)
    patient.identifier = identifierList
    patient.id = "FID" + patientId
    return patient


def createReference(domainResource: dor.DomainResource):
    reference = ref.FHIRReference()
    reference.reference = domainResource.relativePath()
    reference.resource_type = domainResource.resource_type
    return reference


def createCondition(diseaseSeries: DataFrame, patientReference: ref.FHIRReference):
    condition = c.Condition()
    codeableConcept = cc.CodeableConcept()
    codingList = list()
    coding = cdg.Coding()
    coding.code = diseaseSeries['code'].values[0].__str__()
    coding.display = diseaseSeries['preferred_text'].values[0]
    coding.system = "http://snomed.info/sct"
    codingList.append(coding)
    codeableConcept.coding = codingList
    condition.code = codeableConcept
    condition.subject = patientReference
    condition.id = "FID" + str(diseaseSeries['id'].values[0])
    condition.meta
    # FHIR extensions for storing information about: position in clinical document, true-text, confidence-score,
    # negation, confidence, certainty
    extensionList = list()
    # ToDo: Find out which extensions are useful and are not defined in a fhir element
    # Extension for nlp-system
    extensionNLPSystem = ex.Extension()
    extensionNLPSystem.url = "http://text2fhir.org/fhir/extensions/nlp-system-modifier"
    extensionNLPSystem.valueString = "cTakes Version 4.0.0.1"
    extensionList.append(extensionNLPSystem)
    # Extension for nlp-date
    nlpDate = fd.FHIRDate("2021-11-29T11:34:12+01:00")
    extensionNLPDate = ex.Extension()
    extensionNLPDate.url = "http://text2fhir.org/fhir/extensions/nlp-date-modifier"
    extensionNLPDate.valueDateTime = nlpDate
    extensionList.append(extensionNLPDate)
    # Extension for offset
    extensionOffset = ex.Extension()
    extensionOffset.url = "http://text2fhir.org/fhir/extensions/offset-modifier"
    pos_start = qu.Quantity()
    pos_start.value = float(diseaseSeries['pos_start'].values[0])
    pos_end = qu.Quantity()
    pos_end.value = float(diseaseSeries['pos_end'].values[0])
    extensionOffset.valueRange = ra.Range()
    extensionOffset.valueRange.high = pos_end
    extensionOffset.valueRange.low = pos_start
    extensionList.append(extensionOffset)
    # Extension for original-text
    extensionOriginaltext = ex.Extension()
    extensionOriginaltext.url = "http://text2fhir.org/fhir/extensions/originaltext-modifier"
    extensionOriginaltext.valueString = diseaseSeries['true_text'].values[0]
    extensionList.append(extensionOriginaltext)
    # Extension for negation
    extensionNegated = ex.Extension()
    extensionNegated.url = "http://text2fhir.org/fhir/extensions/negated-modifier"
    extensionNegated.valueBoolean = bool(diseaseSeries['negated'].values[0])
    extensionList.append(extensionNegated)
    # Extension for uncertainty
    extensionCertainty = ex.Extension()
    extensionCertainty.url = "http://text2fhir.org/fhir/extensions/uncertainty-modifier"
    extensionCertainty.valueDecimal = diseaseSeries['uncertainty'].values[0]
    extensionList.append(extensionCertainty)
    # Extension for conditional
    extensionConditional = ex.Extension()
    extensionConditional.url = "http://text2fhir.org/fhir/extensions/conditional-modifier"
    extensionConditional.valueBoolean = bool(diseaseSeries['conditional'].values[0])
    extensionList.append(extensionConditional)
    # Extension for confidence
    extensionConfidence = ex.Extension()
    extensionConfidence.url = "http://text2fhir.org/fhir/extensions/confidence-modifier"
    extensionConfidence.valueDecimal = diseaseSeries['confidence'].values[0]
    extensionList.append(extensionConfidence)
    condition.extension = extensionList

    return condition

def createDocumentReference(patientReference: ref.FHIRReference, documentId):
    documentReference = dr.DocumentReference()
    documentReference.id = "Document"+documentId
    documentReference.status = "current"
    documentReference.docStatus = "final"
    codeableConcept = cc.CodeableConcept()
    codingList = list()
    coding = cdg.Coding()
    coding.code = "18842-5"
    coding.display = "Discharge summary"
    coding.system = "http://loinc.org"
    codingList.append(coding)
    codeableConcept.coding = codingList
    documentReference.type = codeableConcept
    documentReference.content