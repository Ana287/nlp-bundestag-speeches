import pandas as pd
from xml.etree import ElementTree as ET
import gender_classification as gc
import glob

def parse_data(filepath: str, speech_data):
    data = ET.parse(filepath)
    root = data.getroot()

    # get date 
    protocol_date = root.find('.//datum').get('date')

    # iterate over the <rede> elements and extract their data
    for speech in root.iter('rede'):

        # get id
        speech_id = speech.get('id')

        # get speech content
        speech_text = speech.text.strip() if speech.text else ''
        for paragraph in speech.iter('p'):
            speech_text += ' ' + paragraph.text.strip() if paragraph.text else ''

        # get speaker info
        speaker = speech.find('.//redner')
        first_name = speaker.find('.//vorname').text
        speaker_name = first_name + ' ' + speaker.find('.//nachname').text
        
        # gender classification
        speaker_gender = gc.get_gender(first_name)


        speaker_role = speaker.find('.//rolle/rolle_lang')
        speaker_party = speaker.find('.//fraktion')

        # get speech comments
        comments = []
        for comment in speech.iter('kommentar'):
            comments.append(comment.text.strip())    
        
        # append all data to speech_data
        speech_data.append({
            'id': speech_id,
            'text': speech_text,
            'date': pd.to_datetime(protocol_date, dayfirst=True),
            'speaker_id': speaker.get('id'),
            'speaker_name': speaker_name,
            'speaker_gender': speaker_gender,
            'speaker_role': speaker_role.text if speaker_role is not None else None,
            'speaker_party': speaker_party.text if speaker_party is not None else None,
            'comments': comments if comments is not None else None
        })

    print("parsed data in " + filepath)

    return speech_data

# MAIN METHOD
def get_data():
    speech_data = []

    # loop over all the XML files in the data directory
    for protocol in glob.glob("open_data/*.xml"):
        speech_data = parse_data(protocol, speech_data)

    # create pandas DataFrame with the extracted data
    df = pd.DataFrame(speech_data)

    print("data frame containing the data mentioned above has been created.")

    return df

if __name__ == "__main__":
    get_data()