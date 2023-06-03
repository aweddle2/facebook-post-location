import spacy
from LocationParser.ParsedPost import ParsedPost

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents


def GetEntities(text):
    doc = nlp(text)

    locations = list(filter(lambda x: x.label_  == "FAC" or x.label_  == "PERSON" , doc.ents))
    costs = list(filter(lambda x: x.label_ == "MONEY", doc.ents))

    # for entity in doc.ents:
    #     print(entity.text, entity.label_)

    # Find named entities, phrases and concepts
    return ParsedPost(text, locations, costs)

