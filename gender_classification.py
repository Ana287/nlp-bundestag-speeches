import gender_guesser.detector as gd
detector = gd.Detector()

# dict for name-to-gender classification
gender_by_name = {}

def get_gender(name: str):
    if name in gender_by_name:
        return gender_by_name[name]
    else:
        # if name is double name, split and take only the first name
        name = name.split()
        gender = detector.get_gender(name[0])
        gender_by_name[name[0]] = gender

    return gender