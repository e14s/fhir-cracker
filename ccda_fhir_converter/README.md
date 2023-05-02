# C-CDA to FHIR Converter

## Initial Converter
1. Aaron697_Brekke496_test.xml is the example C-CDA File
2. Aaron697_Brekke496_real.json is the example FHIR File with all components converted (used for comparison)
3. initial_ccda_fhir_converter.py
    - Peliminary C-CDA to FHIR Converter function
    - This function extracts aspects of the Patient, Encounter, and Observations components from C-CDA File and converts it into FHIR objects. From here, the FHIR objects are put into a bundle and serialized to create new JSON file in FHIR format
    - Args: XML file in C-CDA format.
    - Returns: JSON file in FHIR format with (Patient, Encounter, and Observations) components.
4. test.py
    - This script runs the initial_ccda_fhir_converter function on the Aaron697_Brekke496_test.xml file. The output of this function is written to the test.json file.
5. Aaron697_Brekke496_test_results.json
    - Output of running the converter on the Aaron697_Brekke496_test.xml file.
