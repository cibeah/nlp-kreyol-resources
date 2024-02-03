from bs4 import BeautifulSoup
from pathlib import Path
from spacy.vocab import Vocab
from spacy.language import Language
import requests

BASE_URL = "https://www.potomitan.info/duranty/"
SOMMAIRE_URL = "kreyolad.php"


def download_raw():
    r = requests.get(BASE_URL+SOMMAIRE_URL)
    sommaire = BeautifulSoup(r.text)
    i = 0
    for article in sommaire.find(class_="texteprincipal").find_all("a"):
        name = article["href"]
        if name[-4:] != ".php":
            continue
        ri = requests.get(BASE_URL+name)
        article = BeautifulSoup(ri.text).find(class_="texteprincipal")
        for p in article.find_all(align="center"):
            p.decompose()
        with open(f"datasets/kreyolad/raw/{name.split('.')[0]}.txt", "w", encoding="utf-8") as fp:
            fp.write(article.text)
        i += 1
    print(f"Extracted {i} documents")

def format(path_in, path_out, sentencizer):
    path_in = Path(path_in)
    for file in path_in.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as fp:
            text = fp.read()
        doc = sentencizer(text)
        data = ""
        for sent in doc.sents:
            cleaned_sent = sent.text.strip("\n").strip("\t").strip(" ")
            data += cleaned_sent+"\n"
        with open(path_out, "a", encoding="utf-8") as fout:
            fout.writelines(data)


if __name__ == "__main__":
    folder = "datasets/kreyolad/raw"
    nlp = Language(Vocab())
    nlp.add_pipe("sentencizer")
    path_out = "datasets/kreyolad/mono.mart"
    format(folder, path_out, nlp)