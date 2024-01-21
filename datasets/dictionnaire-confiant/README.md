# Dictionnaire créole martiniquais français - Raphaël Confiant

Martinican Creole-French sentence pairs extracted from the first pages of the dictionary up to letter **N**. Retrieved from [Potomitan.info](https://www.potomitan.info/dictionnaire/)

Files:

- `pairs_mart_fra_sources.csv`, CSV file with columns:
    * `text`: sentence in Martinican Creole
    * `translation`: translation in French
    * `num_words`: number of words
    * `author`: author of the sentence
    * `source`: name of the book [1]
    * `page`: page in the dictionary
    * `line`: line in the dictionary

- `bitexts/*`, TXT files with the sentence pairs in bitext format
    * `data.*`: all data
    * `train\test\eval.*`: train, test, and eval splits

[1] Names are given in abbreviations. An index of abbreviations is available [here](https://www.potomitan.info/dictionnaire/dico3.php#ouvrages1).