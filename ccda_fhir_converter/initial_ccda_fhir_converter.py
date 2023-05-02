import lxml.etree as ET
from fhir.resources.patient import Patient
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.encounter import Encounter
from fhir.resources.observation import Observation
from datetime import datetime
import json

def ccda_to_fhir(file):
    """
        This function extracts aspects of the Patient, Encounter, and Observations components 
        from C-CDA File and converts it into FHIR objects. From here, the FHIR objects are
        put into a bundle and serialized to create new JSON file in FHIR format.

        Args:
            XML file in C-CDA format.

        Returns:
            JSON file in FHIR format with (Patient, Encounter, and Observations) components.
        """

    # Parse CCDA document
    ccda = ET.parse(file)
    root = ccda.getroot()

    # Extract relevant data elements
    d = "{urn:hl7-org:v3}"
    patient_data = root.find(d+"recordTarget").find(d+"patientRole")

    components = root.find(d+"component").find(d+"structuredBody")
    for child in components.findall("*"):
        for item in child.findall("*"):
            for item1 in item.findall(d+"title"):
                if item1.text == 'Diagnostic Results':
                    observation_data = item.findall(d+"entry")
                if item1.text == 'Encounters':
                    encounter_data = item.findall(d+"entry")

    # Extract Functions
    def extract_gender_code(c):
        if c == 'M':
            return 'male'
        elif c == 'W':
            return 'female'
        else:
            return 'other'
        
    def extract_date(d):
        date = datetime.strptime(d, '%Y%m%d%H%M%S')
        formatted_date_str = date.strftime('%Y-%m-%d')
        return formatted_date_str

    ## Create FHIR Resources

    # Patient Resource
    patient = Patient(
        resource_type = "Patient",
        id = "5cbc121b-cd71-4428-b8b7-31e53eba8184",
        name = [
            {"use": "official",
            "family": patient_data.find(d+"patient").find(d+"name").find(d+"family").text,
            "given": [patient_data.find(d+"patient").find(d+"name").find(d+"given").text]
            }
        ],
        gender = extract_gender_code(patient_data.find(d+"patient").find(d+"administrativeGenderCode").attrib["code"]),
        birthDate = extract_date(patient_data.find(d+"patient").find(d+"birthTime").attrib["value"])
    )
    resources = [patient]

    # Observation Resource
    for entry in observation_data:
        components = entry.find(d+"organizer").findall(d+"component")
        for ob in components:
            ob_data = ob.find(d+"observation")
            c_u = ob_data.find(d+"value").attrib["unit"]
            ob = Observation(
                resource_type = "Observation",
                status = True,
                code = {
                    "coding": [],
                    "text": ob_data.find(d+"code").find(d+"translation").attrib["displayName"]
                },
                valueQuantity = {
                    "value": ob_data.find(d+"value").attrib["value"],
                    "unit": c_u,
                    "system": "http://unitsofmeasure.org",
                    "code": c_u
                }
            )
            resources.append(ob)

    # Ecounter Resource
    for entry in encounter_data:
        en_data = entry.find(d+"encounter")
        en = Encounter(
            resource_type = "Encounter",
            status = True,
            type = [
                {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": en_data.find(d+"code").find(d+"translation").attrib["code"],
                        "display": en_data.find(d+"code").find(d+"translation").attrib["displayName"]
                    }],
                    "text": en_data.find(d+"code").find(d+"translation").attrib["displayName"]
                }
            ]
        )
        resources.append(en)

    # Create bundle object
    bundle = Bundle(type = 'collection', entry = [])

    for resource in resources:
        entry = BundleEntry()
        entry.resource = resource
        bundle.entry.append(entry)

    # Write bundle to json file
    with open('test.json', 'w') as f:
        f.write(bundle.json())