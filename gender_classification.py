import gender_guesser.detector as gd
import re
import json

detector = gd.Detector()

# dict for name-to-gender classification
gender_by_name = {}

# read json-file containing custom gender classification
with open('data/custom_gender_map.json', 'r') as json_file:
    gender_map = json.load(json_file)

def get_gender(name: str):
    if name in gender_by_name:
        return gender_by_name[name]
    else:
        # check if name is present in custom gender classification
        for speaker in gender_map:
            if name in speaker['speaker_name']:
                gender_by_name[name] = speaker['speaker_gender']
                return speaker['speaker_gender']

        # if name is double name, split by space or hyphen and take only the first name
        name = re.split(r' |-', name)

        gender = detector.get_gender(name[0])
        gender_by_name[name[0]] = gender

    return gender