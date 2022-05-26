#!/usr/bin/env python3
# Make it execuatble if you want to use the shebang

import pydicom # https://github.com/pydicom/pydicom, sudo python3 -m pip install pydicom
from pydicom.datadict import dictionary_keyword
from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

import time
import datetime
from datetime import datetime

#  Additional tags:  AdditionalPatientHistory, AdmittingDiagnosesDescription, ImageComments, InstitutionName
#  LastMenstrualDate, Occupation, OperatorsName, PatientComments, PatientSize, ReferringPhysicianIdentificationSequence, edit as needed.

mwljson = {


    "SpecificCharacterSet": "ISO_IR 100",
    "Modality": "DX",
    "AccessionNumber": "AccessionNumber",
    "ReferringPhysicianName": "Last^First^Middle",
    "ReferencedStudySequence": [
    	{
        "ReferencedSOPClassUID": "",
        "ReferencedSOPInstanceUID": ""
    	}
    ],
    
    "ReferencedPatientSequence": [
    	{
        "ReferencedSOPClassUID": "",
        "ReferencedSOPInstanceUID": ""
    	}
    ],
    "PatientName": "Last^First^Middle",
    "PatientID": "PatientID",
    "PatientBirthDate": "19710504",
    "PatientSex": "M",
    "PatientAge": "",
    "PatientWeight": "",
    "PregnancyStatus": "",
    "MedicalAlerts": "MedicalAlerts",
    "Allergies": "Allergies",
    "StudyInstanceUID": "",
    "StudyID": "StudyID",
    "RequestingPhysician": "Last^First^Middle",
    "RequestedProcedureDescription": "RequestedProcedureDescription",
    "RequestedProcedureCodeSequence": [
    	{
    		"CodeValue": "1234567890123456",
    		"CodingSchemeDesignator": "1234567890123456",
    		"CodingSchemeVersion": "1234567890123456",
    		"CodeMeaning": "1234567890123456"
    	
    	}
    ],
    "AdmissionID": "AdmissionID",
    "SpecialNeeds": "SpecialNeeds",
    "CurrentPatientLocation": "1234567890123456",
    "PatientState": "PatientState",
    "ScheduledProcedureStepSequence": [
    {
        "Modality": "DX",
        "RequestedContrastAgent": "1234567890123456",
        "ScheduledStationAETitle": "AETitle",
        "ScheduledProcedureStepStartDate": "20220525",
        "ScheduledProcedureStepStartTime": "151004",
        "ScheduledPerformingPhysicianName": "Last^First^Middle",
        "ScheduledProcedureStepDescription": "ScheduledProcedureStepDescription",
        "ScheduledProtocolCodeSequence": [
          {
            "CodeValue": "1234567890123456",
            "CodingSchemeDesignator": "1234567890123456",
            "CodingSchemeVersion": "1234567890123456",
            "CodeMeaning": "1234567890123456"
            
          }
        ],
        "ScheduledProcedureStepID": "X019",
        "ScheduledStationName": "1234567890123456",
        "ScheduledProcedureStepLocation": "X-Ray",
        "PreMedication": "PreMedication",
        "ScheduledProcedureStepStatus": "SCHEDULED"
        
      }
    ],
    "RequestedProcedureID": "1234567890123456",
    "RequestedProcedurePriority": "ROUTINE",
    "PatientTransportArrangements": "1234567890123456",
    "ConfidentialityConstraintOnPatientDataDescription": "1234567890123456"
  }

  
WORKLIST_DIR = ''
  
# METHOD TO CONSTRUCT DATASET FROM JSON, SEE SAMPLE, PASS IN the JSON for the Dataset and a Blank Dataset

def getMWLFromJSON(MWLDict, DataSet):
    
    for key, value in MWLDict.items():
        if (isinstance(value, str) or isinstance(value, int)):
            setattr(DataSet, key, value)
        else: # must be a list or sequence
            # setattr(mwlDataSet, key, Dataset())
            sequence = []
            # Create the Sequence Blank Dataset
            for i in range(len(value)):
                sequenceSet = Dataset()
                sequenceSet = getMWLFromJSON(value[i], sequenceSet)
                sequence.append(sequenceSet)
            setattr(DataSet, key, sequence)
    return DataSet
    
# def MWLFromJSONCreateAndSave(output, uri, **request):
# 
#     if request['method'] != 'POST':
#         output.SendMethodNotAllowed('POST')
#     else:
#         query = json.loads(request['body'])
#         print(json.dumps(query))
#         if not os.path.exists(WORKLIST_DIR):
#             os.makedirs(WORKLIST_DIR)
#         response = dict()
#         print("Making MWL from JSON")
#         dataset = Dataset()
#         dataset = getMWLFromJSON(query, dataset)
#         dataset.is_little_endian = True # 'Dataset.is_little_endian' and 'Dataset.is_implicit_VR' must be set appropriately before saving
#         dataset.is_implicit_VR = True
#         # Set creation date/time
#         dt = datetime.now()
#         dataset.ContentDate = dt.strftime('%Y%m%d')
#         timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
#         dataset.ContentTime = timeStr
#         response = SaveDatasetDB(query, dataset)
#         print("Writing test file", response['filename'])
#         dataset.save_as(WORKLIST_DIR + response['filename'] ,write_like_original=True) # True takes care of not explcitly setting (0002, 0002) MediaStorageSOPClassUID & (0002, 0003) MediaStorageSOPInstanceUID
#         DB = ((".  Saved to PACS DB " + RISDB['MWLdatabase'])  if  response['DB'] else ".  Error Saving to Orthanc RIS")
#         response['status'] = "MWL:  " + response['filename'] + DB
#         output.AnswerBuffer(json.dumps(response, indent = 3), 'application/json')
# 
# orthanc.RegisterRestCallback('/mwl/create_from_json', MWLFromJSONCreateAndSave)


def MWLFromJSONCreateAndSave(sample):

    response = dict()
    print("Making MWL from JSON")
    dataset = Dataset()
    dataset = getMWLFromJSON(sample, dataset)
    dataset.is_little_endian = True # 'Dataset.is_little_endian' and 'Dataset.is_implicit_VR' must be set appropriately before saving
    dataset.is_implicit_VR = True
    # Set creation date/time
    dt = datetime.now()
    dataset.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
    dataset.ContentTime = timeStr
    print(dataset)
    filename = sample['AccessionNumber'] + '.wl'
    dataset.save_as(WORKLIST_DIR + filename ,write_like_original=True)
    

mwl = MWLFromJSONCreateAndSave(mwljson)
    
    
    
