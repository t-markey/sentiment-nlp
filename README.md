# Sentiment analysis using NLP

## About

* Scans documents for frequently repeated words of interest
* Command Line Tool
* Outputs results to CSV & HTML 
* Finds Locations, Countries, Organizations, Events, Persons
* Can additionally search nouns, verbs, and adjectives 
* Omits stop words with ability to add additional as parameters
* Filters dates, percents, numbers, ordinal/cardinal types

## Example

![Example image1](/tests/test_output/nio1.png)
![Example image1](/tests/test_output/nio2.png)


## Installation

Uses:
* pandas [Documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
* spaCy [Documentation](https://spacy.io/usage/linguistic-features)


Starting the virtual environment 
```bash
cd 
pip install pipenv
pipenv shell
```
Installing Dependancies

```bash
pipenv install -r requirements.txt
```

Installing the spaCy model

```bash
pipenv run python -m spacy download en_core_web_sm
```
OR
```bash
python -m spacy download en_core_web_sm
```

OR by adding it to requirements.txt

```
spacy>=2.2.0,<3.0.0
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz#egg=en_core_web_sm
```
A guide on working with with [pipenv](https://realpython.com/pipenv-guide/)
Further guidance on installing spaCy can he found [here](https://spacy.io/usage)


## Basic Usage

Each document to be included in the search shold have it's path given as a parameter when running the below script.  In main.py, each document given as a parameter is instantiated as a Document object.  The Document class uses multiple spaCy objects such as doc, span, matching patterns , and tokens to work with the data.   A dictionary of these doc objects is passed to the Batch class which inherits from the Document class.  Note that the Batch class is initialized with the sum of all text from the documents given as arguments as oppused to the file path in the Document class.

Both a .csv and nicely formatted .html file will be produced and out to the following directory: eigen_test/tests/test_output.  (Currently, outputs will be overwritten if the script is run again)  The file bold.py inserts <strong>  tags to bold the keywords in the html file.

```bash
Run : python3 main.py [path/to/document1] [path/to/document1] ...
python3 main.py ../tests/test_docs/doc1.txt ../tests/test_docs/doc2.txt ../tests/test_docs/doc3.txt ../tests/test_docs/doc4.txt ../tests/test_docs/doc5.txt ../tests/test_docs/doc6.txt
```

## Adjusting parameters

A number of the methods in the Document class could act as useful functions in a [jupyter notebook](https://spacy.io/usage/visualizers) environment with spacy, but below are a few easily adjusted parameters that can be adjusted in the main.py file.

* By Default, [Entities](https://spacy.io/usage/linguistic-features#named-entities) (esentially pronouns), Nouns, Verbs,and Adjectives are all counted for frequency as they could have some relevance.

	To omit one/some/all nouns, verbs, adjectives , adjust the ``` doc_all.set_default_phrases("NVA")``` in main.py to "" for none , "N" for just Nouns

	To exclude the named entities you can just comment out ```doc_all.interesting_entities()``` in main.py.


* The most frequent entries are output in descending order with a defualt amount of keywords being 20.  This can be adjusted here : ```doc_all.set_number_results(20)	``` . Large value may reduce performance drastically ( more optimizaiton needed).

* Adding your own stop words to the defualt list provided can be done by calling the method : ``` doc_all.add_stop(['Let'])	```

* The sentence surrounding the word was capped at 40 words.  This logic is in the ```	def sentence_cropped(self, word):``` method in the Document class, and places the keyword at index 30 of 40 to provide reasonable context within a sentence of excessive length.


## Roadmap
Future features include :
* Scraping recent SEC filings
* Executing diff comparisons on the notes sections of filings
* Topic modeling and Sentiment Analysis using Gensim library



## Data Sanity Checking

Testing that results are within a reasonable tolerance of a simple grep search.

```bash
cd test_docs
grep -roh people . | wc -w     
```

Additionally, this one liner borrowed and modified from [Doug Mcilroy](https://www.cs.tufts.edu/~nr/cs257/archive/don-knuth/pearls-2.pdf) quickly shows the top 200 words in terms of highest frequency (omitting the top 30 as primarily stop words) to get a sense of what a few of the more relevant words might be when troubleshooting.

```bash
cat *.txt >> combined.txt
cat combined.txt | tr -cs A-Za-z '\n' | tr A-Z a-z | sort | uniq -c | sort -rn | sed 230q | tail -n +31
````





