# NLP-Analysis of German Parliamentary Speeches

This repository is part of the thesis entitled "A natural language processing analysis of parliamentary speeches in the German Bundestag from 1949 to 2023 with regards to gender equality and women's politics". The focus of the thesis lies on contrasting the thematic preferences of men and women, as well as their connection to women's political issues based on their speeches and highlighting their historical development. Furthermore, the speakers’ reception in parliament is analyzed and the gender-specific distinguishability of speech style is verified. This repository includes the source code for all the performed analyses.

## Data basis

The plenary protocol data has been extracted from two sources:
- Blaette, Andreas (2017): GermaParl. Corpus of Plenary Protocols of the German Bundestag. TEI files, availables at: https://github.com/PolMine/GermaParlTEI.
- Deutscher Bundestag. Open Data - Plenarprotokolle der 20. Wahlperiode und Stammdaten aller Abgeordneten seit 1949. https://www.bundestag.de/services/opendata

## Repository Content

### Scripts
- `open_data_parser.py`: parses the XML files from the German Bundestag, extracts relevant information and stores it in a pandas DataFrame.
- `germa_parl_parser.py`: parses the XML files from the GermaParl-Corpus, extracts relevant information and stores it in a pandas DataFrame.
- `gender_classification.py`: uses the `gender_guesser` library and `custom_gender_map.json` to determine and return the gender of a given name.
- `assemble_data.py`: merges the two dataframes, cleans and standardizes speaker names and gender classifications, adds IDs and speech lengths and saves the resulting dataframe to a pickled file.
- `create_subdata.py`: divides dataframe into yearly sub-dataframes and saves them to pickled files.

### Notebooks

- `data-exploration.ipynb`: initial data exploration like speech counts, gender distributions and speech length ratios.
- `topic-modelling.ipynb`: training of LDA-model; saves topic distributions for every speech in a new dataframe
- `topic-exploration.ipynb`: explores and plots different statistics surrounding the speech topics and their gender distributions
- `interjection-analysis.ipynb`: quantitative analysis of comments and reactions during the speeches
- `gender-prediction.ipynb`: training of a logistic regression model to predict the gender of a speaker based on their speech
- `revising-genders.ipynb`: check and compare gender classification with standing data from the German Bundestag

### Additional data
- `custom_gender_map.json`: JSON-file containing manually gender-classified names from the speech data
- `member_data.pkl`: member data extracted from the standing data of the German Bundestag
- `parliament_members.json`: JSON-file containing member information on every legislative period

### Reference files
- `comments_per_speech.txt`: text file containing extracted speaker comments for each speech
- `topics.txt`: text file containg a list of all 150 topics in the topic model and their keywords

### Output
- `models/lda_model_150.pkl`: trained topic model with 150 topics
- `models/log.joblib`: trained logistic regression model for gender prediction
- `pyLDAvis/lda_150_topics.html`: web-based visualization of topic model with [pyLDAvis](https://github.com/bmabey/pyLDAvis)

## How to Use

1. Download XML files of interest from the data sources mentioned above
2. Use the parsers `open_data_parser.py` and `germa_parl_parser.py` to extract data
3. Run `assemble_data.py` to clean data and merge it into one single dataframe
4. Run notebooks of interest to perform the different analyses

## Acesss Dataframes

The dataframes resulting from the different analyses have been saved to a pickle format and can be accessed via Zenodo: