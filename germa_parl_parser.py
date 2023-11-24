import pandas as pd
from xml.etree import ElementTree as ET
import gender_classification as gc
import glob

def parse_data(filepath: str, speech_data):
    data = ET.parse(filepath)
    root = data.getroot()

    # get date 
    protocol_date = root.find('.//date').text

    # get legislative period
    legislative_period = root.find('.//legislativePeriod').text

    # iterate over the <rede> elements and extract their data
    for speech in root.iter('sp'):

        # get speech content
        speech_text = speech.text.strip() if speech.text else ''
        for paragraph in speech.iter('p'):
            speech_text += ' ' + paragraph.text.strip() if paragraph.text else ''

        # get speaker info
        speaker_name = speech.get('name').strip()
        if "." in speaker_name.split()[0]:
            first_name = speaker_name.split()[1]
        else:
            first_name = speaker_name.split()[0]
        
        # gender classification
        speaker_gender = gc.get_gender(first_name)

        speaker_role = speech.get('position')
        speaker_party = speech.get('party')

        # get speech comments
        comments = []
        for comment in speech.iter('stage'):
            comments.append(comment.text.strip())    
        
        # append all data to speech_data
        speech_data.append({
            'text': speech_text,
            'date': pd.to_datetime(protocol_date, dayfirst=False),
            'legislative_period': legislative_period,
            'speaker_name': speaker_name,
            'speaker_gender': speaker_gender,
            'speaker_role': speaker_role if speaker_role is not None else None,
            'speaker_party': speaker_party if speaker_party is not None else None,
            'comments': comments if comments is not None else None
        })

    print("parsed data in " + filepath)

    return speech_data

# MAIN METHOD
def get_data():
    speech_data = []

    # loop over all the XML files in the data directory
    for protocol in glob.glob("C:/Users/Ana/OneDrive - Hochschule Düsseldorf/MA/data/germa_parl_data/*.xml"):
        speech_data = parse_data(protocol, speech_data)

    # create pandas DataFrame with the extracted data
    df = pd.DataFrame(speech_data)

    print("data frame containing the data mentioned above has been created.")

    return df

if __name__ == "__main__":
    get_data()