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
    return word.strip(" ();") in INDICATORS


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
                                "text": text.strip(' "'),
                                "translation": translation.strip(' "'),
                                "num_words": line["num_words"],
                                "author": author,
                                "source": source,
                                "page": id_page,
                                "line": line["id"] 
                            }
                        )

    # Create DataFrame and save as csv
    pd.DataFrame(data).to_csv(path_out, index=False)

def get_source_like_item(text):
    item = None
    search = re.search("\((.+)\)", text)  
    if search is not None:
        item = search.group(1).strip()
    # Also look for truncated parentheses
    else:
        search = re.search("\((.+)$", text)
        if search is not None:
            item = search.group(1).strip(" ,-")
        else:
            search = re.search("(.+)\)", text)
            if search is not None:
                item = search.group(1).strip(" ,-")
    return item


def check_dataset(path_in):
    """
    Logs list of sentences to be cleaned
    """
    df = pd.read_csv(path_in)
    # get unique sources
    sources = df.source.unique()
    authors = df.author.unique()
    text_types = ["text", "translation"]
    # check for parentheses - might be badly extracted data
    check_parentheses = df["text"].str.contains("[\(\)]") | df["translation"].str.contains("[\(\)]")
    check_bad_start = df["text"].str.contains("^[^A-Z]")
    problems = df[check_parentheses | check_bad_start]
    for iline, line in problems.iterrows():
        item = get_source_like_item(line["text"])
        log = f"Line {str(iline)}. \n    In text  :"
        if item in sources:
            log += f"{item} in sources"
        elif item in authors:
            log += f"{item} in authors"
        else:
            log += f"{item} - no correspondance"
        log += "\n    In translation  :"
        item = get_source_like_item(line["translation"])
        if item in sources:
            log += f"{item} in sources"
        elif item in authors:
            log += f"{item} in authors"
        else:
            log += f"{item} - no correspondance"
        print(log)
    return problems.shape[0]

def write_bibtexts(path_in, path_out):
    path_out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(path_in)
    with open(path_out / "train.mart1259", "w", encoding="utf-8") as f:
        f.write("\n".join(list(df["text"].str.strip(' "').values)))
    with open(path_out / "train.fra", "w", encoding="utf-8") as f:
        f.writelines("\n".join(list(df["translation"].str.strip(' "').values)))

if __name__ == "__main__":
    path_in = Path("../nlp-kreyol/dico_creole_a_n__confiant_avant_publi_papier.pdf")
    path_out = Path("datasets/dictionnaire-confiant/confiant_mqc.csv")
    path_clean = path_out.parent / (str(path_out.stem) +  "_clean" + path_out.suffix)
    path_bibtext = path_clean.parent / "bibtext"
    # create_raw_dataset(path_in, path_out)
    # num_anomalies = check_dataset(path_clean)
    # print(num_anomalies, "anomalies detected")
    write_bibtexts(path_clean, path_bibtext)