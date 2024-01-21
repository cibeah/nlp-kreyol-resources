### Tatoeba

Guadeloupean Creole-French-English sentence triplets retrived from [Tatoeba](https://tatoeba.org)

Files:

- `triplets_gcf_fra_eng.csv`, original CSV file with columns:
    * `id`: sentence ID on Tatoeba
    * `lang`: language ID on Tatoeba (== `gcf`)
    * `sentence`: sentence in Guadeloupean Creole
    * `sentence_fra`: translation in French
    * `sentence_eng`: translation in English

*Note*: When several translations are available in or two languages, each possible translation triplet corresponds to a new row.

- `pairs_gcf_fra.csv`, CSV file with columns:
    * `sentence`: sentence in Guadeloupean Creole
    * `sentence_fra`: translation in French

- `bitexts/*`, TXT files with the Creole-French sentence pairs in bitext format
    * `train\test\eval.*`: train, test, and eval splits