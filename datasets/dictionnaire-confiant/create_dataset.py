import re

import pandas as pd
from pathlib import Path
import pdfplumber

# List of all abbreviations found on https://www.potomitan.info/dictionnaire/dico4.php
# + others found in the documents and "Dictionnaire" to remove the headers/lowers
INDICATORS = [
    "afr.","ang.","arch.","arg.", "ayt.", 
    "car.","cit.","dom.","enf.","esp.","exp.", 
    "fém.", "f. r.", "f.r.a.","gwd","guy.",
    "iron.","lit.","masc.", "mél.", "n. sc.", 
    "néol.","on.", "péj.","pvb.","r.", "st-l.",
    "syn.","tam.","var.",
    "Dictionnaire", "sue.", "port.", "iron.", "ex.", 
    "lit.", "rép.", "it.", "all."
]

SOURCE_PATTERN = '(.+) ?\((.+), (.+)\)'
SOURCE_PATTERN_1 = '(.+) ?\((.+) (.+)\)'
ZOOMIN_SOURCE_PATTERN = '\((.+), (.+)\)'
CHARACTER_HEIGHT = 10

def is_a_bold_letter(char):
    is_a_letter = char["text"].isalpha()
    is_lower_case = char["text"].lower() == char["text"]
    is_bold = char["fontname"].find("Bold") > -1
    return is_a_letter and is_lower_case and is_bold

def is_indicator(word):
    """
    Check whether word is indicator
    """
    return word.strip(" ();.") in INDICATORS


#TODO: add separate run to handle 'rép.' and 'pvb.' translations


def create_raw_dataset(path_in, path_out):
    data = []
    with pdfplumber.open(path_in) as pdf:
        for id_page, page in enumerate(pdf.pages):
            page_data = []
            last_line_y, last_line_height = page.bbox[-1], 1
            char_aggreg = []
            has_bold_letters = False
            id_data = 0
            for char in page.chars:
                # if (char["y0"] < last_line_y - last_line_height/2) or (char["y0"] > last_line_y + last_line_height/2):
                if (char["y0"] < last_line_y - CHARACTER_HEIGHT) or (char["y0"] > last_line_y + CHARACTER_HEIGHT):
                    # If last line had bold chars, add it as an extracted sentence
                    text = "".join(char_aggreg).strip()
                    # clean spaces
                    words = [word for word in text.split(" ") if word.strip()]
                    text = " ".join(words).strip()

                    num_words = len(words)
                    has_indicator = any([is_indicator(word) for word in words])
                    page_data.append({
                        "id": id_data,
                        "text": text,
                        "num_words": num_words,
                        "is_bold": has_bold_letters,
                        "is_example": has_bold_letters and (num_words>2) and not has_indicator,
                        "is_indication": has_indicator, # has_bold_letters
                        "is_word": has_bold_letters and (num_words==1),
                        "is_source": re.search(SOURCE_PATTERN, text) is not None
                    })
                    id_data += 1
                    
                    # Init new line
                    last_line_y = char["y0"]
                    last_line_height = char["height"]
                    char_aggreg = []
                    has_bold_letters = False
                
                has_bold_letters = has_bold_letters or is_a_bold_letter(char)
                char_aggreg.append(char["text"])
            
            # Extract data for examples and translations
            num_page_items = len(page_data)
            for i in range(num_page_items-1):
                if page_data[i]["is_example"]:
                    line, next_line = page_data[i], page_data[i+1]
                    if not (next_line["is_bold"] | (next_line["num_words"]<2)):
                        text, author, source = line["text"], None, None
                        translation_line = 1 #translation starts on next line 
                        # If the previous line was also an example, consider
                        # it a single example
                        if (i > 1) and (page_data[i-1]["is_example"]):
                            text = page_data[i-1]["text"] + " " + text

                        # Look for a source
                        result = re.search(SOURCE_PATTERN, text)
                        if result is not None:
                            text = result.group(1).strip(' "')
                            author = result.group(2).strip()
                            source = result.group(3).strip()
                        else:
                            # Look for source with slightly different pattern
                            result = re.search(SOURCE_PATTERN_1, text)
                            if result is not None:
                                text = result.group(1).strip(' "')
                                author = result.group(2).strip()
                                source = result.group(3).strip()
                            # If there is still no source, it might be on the next line
                            # the translation should then be on the line after
                            # Breaks if an example takes on two FULL lines with the source on a
                            # third line, but this should not happen
                            elif (i+2 < num_page_items) and not (page_data[i+2]["is_bold"]):
                                result = re.search(ZOOMIN_SOURCE_PATTERN, next_line["text"])
                                if result is not None:
                                    author = result.group(1).strip()
                                    source = result.group(2).strip()
                                    translation = page_data[i+2]["text"]
                                    translation_line = 2
                        
                        # add 1 or 2 lines of translation after source 
                        translation =  page_data[i+translation_line]["text"]
                        if (
                            (i+translation_line+1 < num_page_items) 
                            and not (page_data[i+translation_line+1]["is_bold"])
                            and not (page_data[i+translation_line+1]["is_indication"])
                        ):
                            translation += " " + page_data[i+translation_line+1]["text"].strip()

                        data.append({
                                "text": text.strip(' ".'),
                                "translation": translation.strip(' ".'),
                                "num_words": line["num_words"],
                                "author": author,
                                "source": source,
                                "page": id_page,
                                "line": line["id"] 
                            }
                        )

    # Create DataFrame and save as csv
    pd.DataFrame(data).to_csv(path_out, index=False)

def clean_dataset(path_in, path_out):
    df = pd.read_csv(path_in)

    # get unique sources
    sources = df.source.unique()
    authors = df.author.unique()

    # check for parentheses - might be badly extracted data
    for iline, line in df[df.text.str.contains("\(")].iterrows():
        search = re.search("\((.+)\)", line["text"])  
        if search is not None:
            item = search.group(1).strip()
        else:
            search = re.search("\((.+)$", line["text"])
            if search is not None:
                item = search.group(1)
        print(item)
        source_search = re.search("\((.+)\)", item)  
    df.to_csv(path_out, index=False)

path_in = Path("PATH_TO_PDF")
path_out = Path("datasets/dictionnaire-confiant/confiant_mqc.csv")
# create_raw_dataset(path_in, path_out)
clean_dataset(path_out, path_out.parent / (str(path_out.stem) +  "_clean" + path_out.suffix))