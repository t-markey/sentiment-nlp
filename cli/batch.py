from document import Document 
import spacy
from spacy.matcher import Matcher
from collections import Counter
import pprint
import pandas as pd 


class Batch(Document):

	
	def __init__(self, all_text):
		
		self.nlp = spacy.load("en_core_web_sm")
		self.clean_name = "All_text"
		self.doc = self.nlp(all_text)
		# Default 326 stop words in spacy
		self.all_stopwords = self.nlp.Defaults.stop_words
		self.max_results = 100
		# Default include nounss in search
		self.default_phrase_speech = ''
		self.meaningful_words= []



	# Takes in dict of the concatonated document objects
	# Can search all docs, but then pass dict of just one doc to search only 1
	def add_dict_file_objects(self, dict_input):
		self.dict_doc_objects = dict_input


	# Show frequency of all words in the document
	def output_all_freq_relevant(self):
		t = [tok.text for tok in self.doc if tok.is_punct != True and tok.is_stop != True and tok.text in self.meaningful_words ]
		frequency = Counter(t)
		top_common = frequency.most_common(self.max_results) # Returns a tuple ("Keyword", Frequency)
		return top_common

	


	# Crops sentences down to under 40 words
	# Takes input of keyword string and outputs list of sentences  
	def sentence_cropped(self, word, docu_object):
		self.doc= docu_object
		sentence_list = []
		matcher = Matcher(self.nlp.vocab)
		pattern = [{ "TEXT": word }]
		matcher.add("Getting token",[pattern])
		match = matcher(self.doc)
		#print(f"There is {len(match)} matches")
		
		# m[1] is an int retunred by matching representing index of keyword in this sentence
		for m in match: 
			full_sentence = self.doc[m[1]].sent
			if len(full_sentence) < 40:	# sentence is short enough to use entire
				sentence_list.append(self.doc[m[1]].sent.text )
			
			# Sentence Too long AND Match word is first word in sentence, goes 40 words from this if exists
			elif (len(full_sentence) >= 40 and full_sentence.start == m[1]):
				try:
					end_span_index = 40
				except:
					end_span_index = full_sentence.end
						
				span = full_sentence[0:end_span_index]
				sentence_list.append(span.text ) 
		
			# Too long, Not first word , go 30 before, 10 after if exists
			# Else Just go 40 back  
			else:
				try: 
					span = self.doc[m[1]-30:m[1] +9]
					sentence_list.append("..." + span.text + "..." )
					
				except:
					span = self.doc[m[1]-40 : m[1] + 1 ]
					sentence_list.append("..." + span.text )

		return sentence_list





	# Show frequency of all words in the document
	# Returns a dataframe
	def output_targetted(self):
		t = [tok.text for tok in self.doc if tok.is_punct != True and tok.is_stop != True and tok.text in self.meaningful_words ]
		frequency = Counter(t)
		top_common = frequency.most_common(self.max_results) # Returns a tuple ("Keyword", Frequency)
		
		# Colummns Word, Frequency Document Name, Relevant sentence
		w = []
		d = []
		s = []
		f = []

		# Loop over loaded documents
		for key, value in self.dict_doc_objects.items():
			
			# Get doc object for each document
			doc_from_dict =self.dict_doc_objects[key].get_doc()

			# loop over top words
			for i, top_word in enumerate(top_common):
				# loop over all matches of that wrod in document and crop relevant sentence
				for occurance in self.sentence_cropped(top_word[0], doc_from_dict):
					w.append(top_word[0] )
					occurance = occurance.replace('\n', ' ')
					occurance = occurance.replace('\t', ' ')
					s.append(occurance)
					d.append(key)
					f.append(top_word[1])

			
			#print(key +" has been processed. ")		
	
		df = pd.DataFrame({"Word": w,"Frequency": f,"Document Name": d,"Sentence": s })
		df = df.sort_values(['Frequency'], ascending=False)
		df = df.reset_index(drop=True)

		return df
			

		







