import argparse

import numpy as np
import pandas as pd
from pathlib import Path
import requests

# To retieve online via API request
TATOEBA_URL = 'https://tatoeba.org/eng/api_v0/search?from={}&count={}&word_count_min={}&word_count_max={}'

# To extract from local .tsv files downloaded at `https://tatoeba.org/fr/downloads`
ROOT_DATA = Path("sentences")
LINK_PATH = Path("sentences/link/sentences_base.csv")
TRANSLATION_LANGS = ["fra", "eng"]

parser = argparse.ArgumentParser(description='create dataset from tatoeba data')
parser.add_argument('--offline', action="store_true", 
                    help='Read data from local .tsv files')
parser.add_argument('--bitext', action="store_true", 
                    help='Read data from local .tsv files')


def get_sentences_from_api(lang, translation_langs=TRANSLATION_LANGS, max_items=int(1e5), max_word_count=100):
    
    def filter_results(results):
        cleaned_results = []
        for result in results:
            # Filter results to keep the translations from languages 
            # specificed in `translation_langs`
            item = {
                "id": result["id"],
                "lang": result["lang"],
                "sentence": result["text"]
            }
            for lang in translation_langs:
                item["sentence_"+lang] = [
                    trad["text"] 
                    for trad_set in result["translations"]
                    for trad in trad_set 
                    if trad["lang"] == lang
                ]
            cleaned_results.append(item)
        return cleaned_results

    data = []
    counter = 0
    # API returns max 1000 results for one request, so 
    # we split our request per word count to get more
    for word_count in range(1, max_word_count+1):
        next_page, page = True, 0
        while (next_page) and (counter < max_items):
            page += 1
            r = requests.get(TATOEBA_URL.format(lang, max_items, word_count, word_count)+"&page="+str(page))
            req = r.json()
            paging, results = req["paging"], req["results"]
            next_page = paging["Sentences"]["nextPage"]
            counter += paging["Sentences"]["current"]
            page = paging["Sentences"]["page"]
            data.extend(filter_results(results))

    print(f'Extracted {counter} sentences from Tatoeba')

    df = pd.DataFrame(data)
    for lang in translation_langs:
        df = df.explode("sentence_"+lang)
    return df.drop_duplicates()

def get_sentences_from_tsv(lang, root_path, link_path, translation_langs=TRANSLATION_LANGS):
    columns = ["lang", "sentence"]
    link_df = pd.read_csv(link_path, header=None, sep="\t", na_values="\\N")
    # Drop sentences with no known link
    link_df = link_df.dropna()
    # Drop original sentences
    link_df = link_df[link_df.iloc[:,1]!=0]
    link_df = link_df.astype(np.int32)
    link_df.columns = ["to", "from"]

    # Read target language data
    df = pd.read_csv(root_path / lang / "sentences.tsv", header=None, sep="\t").set_index(0)
    df.columns = columns
    # Get ID of any translation
    df = df.merge(link_df.set_index('to'), how="left", left_index=True, right_index=True)
    df = df.merge(link_df.set_index('from'), how="left", left_index=True, right_index=True)
    base_columns = df.columns

    for tlang in translation_langs:
        df0 = pd.read_csv(root_path / tlang / "sentences.tsv", header=None, sep="\t").set_index(0)
        suffix = df0.iloc[0,0]
        df0.columns = columns
        df0.columns = df0.columns + "_" + suffix
        df = df.merge(df0.iloc[:,1], how="left", left_on="from", right_index=True)
        df = df.merge(df0.iloc[:,1], how="left", left_on="to", right_index=True)
        df = df.melt(id_vars=base_columns, value_name="sentence_"+suffix,
                    value_vars=df.columns[df.columns.str.contains(suffix)])
        base_columns = list(base_columns)+ ["sentence_"+suffix]

    df = df.drop(["from", "to", "variable"], axis=1)
    return df

def write_bitexts(path_in, path_out, lang_out=["fra", "eng"]):
    path_out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(path_in)
    to_escape = ["\u202f"]
    for lang in lang_out:
        data = df.loc[~pd.isna(df[f"sentence_{lang}"]), ["sentence", f"sentence_{lang}"]].drop_duplicates()
        for char in to_escape:
            data["sentence"] = data["sentence"].str.replace(char, " ")
            data[f"sentence_{lang}"] = data[f"sentence_{lang}"].str.replace(char, " ")
        data = data.drop_duplicates()
        (path_out / f"gcf--{lang}").mkdir(parents=True, exist_ok=True)
        with open(path_out / f"gcf--{lang}" / "train.gcf", "w", encoding="utf-8") as f:
            f.write("\n".join(list(data["sentence"].str.strip(' "').values)))
        with open(path_out / f"gcf--{lang}" / f"train.{lang}", "w", encoding="utf-8") as f:
            f.writelines("\n".join(list(data[f"sentence_{lang}"].str.strip(' "').values)))

if __name__ == "__main__":
    args = parser.parse_args()
    # if args.offline:
    #     df = get_sentences_from_tsv(
    #         lang="gcf", root_path=ROOT_DATA, link_path=LINK_PATH,
    #         translation_langs=TRANSLATION_LANGS
    #     )
    # else:
    #     df = get_sentences_from_api(lang="gcf", max_word_count=100)
    # df.to_csv("tatoeba_gcf.csv", index=False)
    if args.bitext:    
        write_bitexts(
            Path("datasets/tatoeba/tatoeba_gcf.csv"), 
            Path("datasets/tatoeba/bitext"), 
            lang_out=["fra"]
        )

