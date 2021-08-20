import pydicom # https://github.com/pydicom/pydicom, sudo python3 -m pip install pydicom
from pydicom.datadict import dictionary_keyword
from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

import time
import datetime
from datetime import datetime


mwljson = {
    "AccessionNumber": "DEVACC00000077",
    "AdditionalPatientHistory": "Test thigh",
    "AdmittingDiagnosesDescription": "A01.02,A02.29,C25.0,C43.72,C44.709,C44.722",
    "Allergies": "",
    "ContentDate": "20210817",
    "ContentTime": "133959.674187",
    "ImageComments": "Tech:  SP",
    "InstitutionName": "",
    "LastMenstrualDate": "",
    "MedicalAlerts": "",
    "Modality": "MR",
    "Occupation": "",
    "OperatorsName": "Tech^SDS",
    "PatientBirthDate": "19571116",
    "PatientComments": "",
    "PatientID": "DEV0000002",
    "PatientName": "Mouse^Mickey^LIttle",
    "PatientSex": "M",
    "PatientSize": "",
    "PatientWeight": "",
    "ReferencedStudySequence": [],
    "ReferringPhysicianIdentificationSequence": [
      {
        "InstitutionName": "",
        "PersonIdentificationCodeSequence": [
          {
            "CodeMeaning": "Local Code",
            "CodeValue": "0002",
            "CodingSchemeDesignator": "L"
          }
        ],
        "PersonTelephoneNumbers": "^WPN^CP^"
      }
    ],
    "ReferringPhysicianName": "0002:^^",
    "RequestedProcedureDescription": "TIBIA AND FIBULA W/WO (R)",
    "RequestedProcedureID": "0030",
    "ScheduledProcedureStepSequence": [
      {
        "Modality": "MR",
        "RequestedProcedureID": "0030",
        "ScheduledProcedureStepDescription": "TIBIA AND FIBULA W/WO (R)",
        "ScheduledProcedureStepID": "0030",
        "ScheduledProcedureStepStartDate": "20210817",
        "ScheduledProcedureStepStartTime": "090000",
        "ScheduledProtocolCodeSequence": [
          {
            "CodeMeaning": "[\"73720\",\"A9579\"]",
            "CodeValue": "0030",
            "CodingSchemeDesignator": "C4"
          }
        ],
        "ScheduledStationAETitle": "NmrEsaote"
      }
    ],
    "SpecificCharacterSet": "ISO_IR 192",
    "StudyDescription": "TIBIA AND FIBULA W/WO (R)",
    "StudyInstanceUID": "1.3.6.1.4.1.56016.0.1.1.175.1629207598"
  }
  
WORKLIST_DIR = '/Users/sscotti/Desktop/ORTHANC_DOCKER_RIS/MWL/'
  
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
    
    
    
