# nlp-kreyol-resources
List of useful resources (dictionaries, corpora, papers, models, etc.) to work on NLP for french-based Caribbean creoles and similar creole languages

## Datasets :open_file_folder:
### Ready-to-use
Open source annotated corpora.

### Other corpora resources
#### > Written

* **Tatoeba** [[link](https://tatoeba.org/fr/sentences/show_all_in/gcf/und)]

    2 123 sentences in Guadeloupean creole with translations for some (English, French).

* **Kréyolad** [[link](https://www.potomitan.info/duranty/kreyolad.php)]

    All contributions of Jude Duranty to the newspaper Antilla from 2004 to 2023

#### > Oral

* **CREOLORAL** [[link](http://ircom.huma-num.fr/site/description_projet.php?projet=creoloral)] (**Not open source**)

  *Anne Zribi-Hertz, Emmanuel Schang, Herby Glaude*

  2012

  3 hours of oral data, spontaneously spoken MQ & GP creole, with transcriptions and french translations. Not open source but is (partially ?) available here (with no annotations ?) [[link](https://cocoon.huma-num.fr/exist/crdo/search2.xql?page=1&max=500&lang=fr&nonce=MTcyODE4Mg%3D%3D&language=http%3A%2F%2Flexvo.org%2Fid%2Fiso639-3%2Fgcf), 19 audio records]

* **Pawolotek** [[link](https://pawolotek.com/index.php/podcast-category/extraits/)]

  *Simone Lagrand, "Titak - Panorama sonore du parler martiniquais"*

  2022

  45 short audio files in Martinican creole (a few seconds/minutes long) recorded in Martinique.

#### > Unrealeased

Tracking unreleased corpora.

* Data for **Noun Phrases in mixed Martinican Creole and French: Evidence for an Underspecified Language Model**

    *Christelle Lengrai, Juliette Moustin, Pascal Vaillant*

    Data recorded on radio broadcasts in Martinique in 2005-2006. Transcribed and annotated.

    2016

* Data for **How to Parse a Creole: When Martinican Creole Meets French**
 
    Martinican creole tree bank: 240 fully annotated sentences. Not publicly available.

    2022


## Models :chart_with_upwards_trend:

### Classification

* **Guadeloupean Creole Language Identification Tool** [[link](https://gitlab.com/williamsotomartinez/gclit/)]

    2020, William Soto

### Translation
* **CreoleM2M** [[link](https://huggingface.co/prajdabre/CreoleM2M)]

    2023, Raj Dabre

    Multilingual translation model built with HuggingFace. Support for 26 creoles including **Saint Lucian, Seychellois, Mauritian, Haitian** creoles. Online playground available [here](https://huggingface.co/spaces/prajdabre/CreoleM2M).

### Speech Recognition & Query 
    
* **ASR + Query-by-Example** [[link](https://github.com/macairececile/ASR-QbE-creole)]
    
    2022, Cécile Macaire et al
   
   **Guadeloupean and Mauritian creole**. Goal: design linguistic tools for language documentation 
  
## Papers :page_with_curl:

### Building Datasets & Corpora
    
#### French-based

* **Case Study on Data Collection of Kreol Morisien, a Low-Resourced Creole Language** [[link](https://ieeexplore.ieee.org/document/9845658)]

   *David Joshen Bastien, Vijay Prakash Chumroo, Johan Patrice Bastien*

    2022, IST-Africa Conference

* **MorisienMT: A Dataset for Mauritian Creole Machine Translation** [[paper](https://arxiv.org/abs/2206.02421), [dataset](https://huggingface.co/datasets/prajdabre/KreolMorisienMT)]

    *Raj Dabre, Aneerav Sukhoo*

    2022

* **Krik: First Steps into Crowdsourcing POS tags for Kréyòl Gwadloupéyen** [[link](https://hal.science/hal-01790617)]

   *Alice Millour, Karën Fort*

  2018
  
#### Others

  * **JamPatoisNLI: A Jamaican Patois Natural Language Inference Dataset** [[link](https://arxiv.org/abs/2212.03419)]

    *Ruth-Ann Armstrong, John Hewitt, Christopher Manning*

    2022

### Classification

#### French-based 

* **Language Identification of Guadeloupean Creole** [[paper](https://hal.science/hal-03047144/document), [code](https://gitlab.com/williamsotomartinez/gclit/)]

  *William Soto*

  2020

### POS Tagging 

* **Krik: First Steps into Crowdsourcing POS tags for Kréyòl Gwadloupéyen** [[link](https://hal.science/hal-01790617)]

   *Alice Millour, Karën Fort*

  2018

* **How to Parse a Creole: When Martinican Creole Meets French** [[link](https://aclanthology.org/2022.coling-1.387.pdf)]

    *Ludovic Mompelat, Daniel Dakota, Sandra Kübler*

    2022

### Translation 

#### French-based 

* **Kreol Morisien to English and English to Kreol Morisien Translation System using Attention and Transformer Model** [[link](https://journal.uob.edu.bh/bitstream/handle/123456789/3918/paper%2012.pdf)]

    *Zaheenah Boodeea, Sameerchand Pudaruth* 

    2020

### Speech Recognition

* **Automatic Speech Recognition and Query By Example for Creole Languages Documentation** [[link](https://hal.science/hal-03625303/document), [code](https://github.com/macairececile/ASR-QbE-creole)]

    *Cécile Macaire, Didier Schwab, Benjamin Lecouteux, Emmanuel Schang*

    2022

    Guadeloupean & Mauritian Creoles

#### Others

### General 

* **On Language Models for Creoles** [[link](https://arxiv.org/abs/2305.13246)]

   *Heather Lent, Emanuele Bugliarello, Miryam de Lhoneux, Chen Qiu, Anders Søgaar* 

   2021, Conference on Computational Natural Language Learning 

* **What a Creole Wants, What a Creole Needs**  [[link](https://arxiv.org/abs/2206.00437)]

    *Heather Lent, Kelechi Ogueji, Miryam de Lhoneux, Orevaoghene Ahia, Anders Søgaard*

   2022

* **Ancestor-to-Creole Transfer is Not a Walk in the Park** [[link](https://arxiv.org/abs/2206.04371)]

    *Heather Lent, Emanuele Bugliarello, Anders Søgaard*

    2022

* **African Substrates Rather Than European Lexifiers to Augment African-diaspora Creole Translation** [[link](https://openreview.net/pdf?id=YKUv4sSOom)]

  *Nathaniel Romney Robinson, Nathaniel Romney Robinson, Matthew Dean Stutzman, Stephen D. Richardson, David R Mortensen*

  2023


### Other

* **Une grammaire formelle du créole martiniquais pour la génération automatique** [[link](https://aclanthology.org/2003.jeptalnrecital-long.24)]

  Pascal Vaillant

  2003
