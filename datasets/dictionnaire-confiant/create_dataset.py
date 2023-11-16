import re

import pandas as pd
import pdfplumber

path = "PATH_TO_PDF"


# List of all abbreviations found on https://www.potomitan.info/dictionnaire/dico4.php
# + others found in the documents and "Dictionnaire" to remove the headers/lowers
INDICATORS = [
    "afr.","ang.","arch.","arg.", "ayt.", 
    "car.","cit.","dom.","enf.","esp.","exp.", 
    "fém.", "f. r.", "f.r.a.","gwd","guy.",
    "iron.","lit.","masc.", "mél.", "n. sc.", 
    "néol.","on.", "péj.","pvb.","r.", "st-l.",
    "syn.","tam.","var.",
    "Dictionnaire", "sue.", "port."
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
    return word.strip(" ();") in INDICATORS

data = []
with pdfplumber.open(path) as pdf:
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
                words = text.split(" ")
                num_words = len(words)
                has_indicator = any([is_indicator(word) for word in words])
                page_data.append({
                    "id": id_data,
                    "text": text,
                    "num_words": num_words,
                    "is_bold": has_bold_letters,
                    "is_example": has_bold_letters and (num_words>2) and not has_indicator,
                    "is_indication": has_bold_letters and has_indicator,
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

        for i in range(len(page_data)-1):
            if page_data[i]["is_example"]:
                line, next_line = page_data[i], page_data[i+1]
                if not (next_line["is_bold"] | (next_line["num_words"]<2)):
                    text, author, source = line["text"], None, None
                    translation = next_line["text"]
                    # If the previous line was also an example, consider
                    # it a single example
                    if (i > 1) and (page_data[i-1]["is_example"]):
                        text = page_data[i-1]["text"] + " " + text
                        # and assume the translation might also be
                        # on 2 lines (maybe not optimal)
                        if (i+2 < len(page_data)) and not (page_data[i+2]["is_bold"]):
                            translation = translation + page_data[i+2]["text"]

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
                        elif (i+2 < len(page_data)) and not (page_data[i+2]["is_bold"]):
                            result = re.search(ZOOMIN_SOURCE_PATTERN, next_line["text"])
                            if result is not None:
                                author = result.group(1).strip()
                                source = result.group(2).strip()
                                translation = page_data[i+2]["text"]

                    data.append({
                            "text": text,
                            "translation": translation,
                            "num_words": line["num_words"],
                            "author": author,
                            "source": source,
                            "page": id_page,
                            "line": line["id"] 
                        }
                    )

# Create DataFrame and save as csv
pd.DataFrame(data).to_csv("datasets/dictionnaire-confiant/confiant_mqc.csv", index=False)