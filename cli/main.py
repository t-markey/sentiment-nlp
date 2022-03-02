import os
import sys
from document import Document 
import pprint
from batch import Batch 
from bold import bold_keywords


#  Run : python3 main.py [path/to/document1] [path/to/document1] ...
#  python3 main.py ../tests/test_docs/doc1.txt ../tests/test_docs/doc2.txt ../tests/test_docs/doc3.txt ../tests/test_docs/doc4.txt ../tests/test_docs/doc5.txt ../tests/test_docs/doc6.txt



# Spacy Doc objects are stored in dictionary to be passed to Batch object
dict_files = {}
for d in sys.argv[1:]: 				# first argument is filename
	d = Document(d)					# Instance for each document input as argument
	d.add_stop(['Let'])				# Example Usage adding "Let" to list of stop words
	dict_files[repr(d)] = d         # Keys are the filename 




# Joining the text of all files to be input to searchable Batch object
all_file_text = ""
for docu in sys.argv[1:]:
	with open(docu , 'r') as file:
		all_file_text += file.read()



# Instantiate Batch object with options
doc_all = Batch(all_file_text)
doc_all.set_default_phrases("NVA")	# Include frequent Verbs, Adjectives, Nouns
doc_all.additional_interest()		# Add Verbs, Adjectives, Nouns to scope of search
doc_all.interesting_entities()		# Add main entities (all pronouns)
doc_all.set_number_results(20)		# Change number of top results to output
doc_all.add_stop(['Let'])			# Example Usage adding "Let" to list of stop words
print(f"Top {doc_all.max_results} Keywords : ")
pprint.pprint(doc_all.output_all_freq_relevant())
doc_all.add_dict_file_objects(dict_files)	# Passes Dictionary of Doc objects to Batch
batch_results = doc_all.output_targetted()  # Storing results in dataframe
pprint.pprint(batch_results)



# Output dataframe to CSV
csv = batch_results.to_csv ('../tests/test_output/test_batch.csv', index = False)

# Outputting dataframe to html file
html = batch_results.to_html()
f = open('../tests/test_output/test_batch.html', 'w')
f.write(html)
f.close()
bold_keywords('../tests/test_output/test_batch.html')

print("\n - CSV and HTML table written to nlp/tests/testoutput -")











