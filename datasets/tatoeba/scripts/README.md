### Dataset creation from Tatoeba

```
cd datasets/tatoeba

python create_dataset.py
OR python create_dataset.py --offline
```

#### Online (better)

Creates dataset from API request to `https://tatoeba.org/eng/api_v0`.
```
python create_dataset.py
```

#### Offline

For datasets downloaded from [https://tatoeba.org/fr/downloads](https://tatoeba.org/fr/downloads)

* ``ROOT_DATA`` = path to root folder with downloaded datasets
* ``LINK_PATH`` = path to base .tsv file linking translation pairs (`sentences_base.tar.bz2`)
* ``TRANSLATION_LANGS`` = [list of downloaded languages for translation pairs]

*Example*:

```
TRANSLATION_LANGS = ["eng", "fra"]
```

Folder structure:
```
ROOT_DATA
├── eng
│   ├── sentences.tsv
├── fra
│   ├── sentences.tsv
├── gcf
│   ├── sentences.tsv
```

Command:
```
python create_dataset.py --offline
```