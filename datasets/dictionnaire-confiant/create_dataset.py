import re

import pandas as pd
import pdfplumber

path = "PATH_TO_PDF"

INDICATORS = ["var.", "syn.", "exp.", "pvb.", "gwd.", "Dictionnaire", ". (arch.)"]
SOURCE_PATTERN = '(.+) ?\((.+), (.+)\)'
SOURCE_PATTERN_1 = '(.+) ?\((.+) (.+)\)'
ZOOMIN_SOURCE_PATTERN = '\((.+), (.+)\)'

def is_a_bold_letter(char):
    is_a_letter = char["text"].isalpha()
    is_lower_case = char["text"].lower() == char["text"]
    is_bold = char["fontname"].find("Bold") > -1
    return is_a_letter and is_lower_case and is_bold

def is_indicator(word):
    """
    Check whether word is indicator
    """
    return word in INDICATORS

data = []
with pdfplumber.open(path) as pdf:
    for id_page, page in enumerate(pdf.pages):
        page_data = []
        last_line_y, last_line_height = page.bbox[-1], 1
        char_aggreg = []
        has_bold_letters = False
        id_data = 0
        for char in page.chars:
            if (char["y0"] < last_line_y - last_line_height/2) or (char["y0"] > last_line_y + last_line_height/2):
                # If last line had bold chars, add it as an extracted sentence
                text = "".join(char_aggreg).strip()
                words = text.split(" ")
                num_words = len(words)
                has_indicator = is_indicator(words[0])
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
                if not (next_line["is_bold"] | (num_words<2)):
                    # Look for a source
                    text, author, source = line["text"], None, None
                    translation = next_line["text"]
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