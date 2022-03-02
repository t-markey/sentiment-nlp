import os
import sys
import spacy
from spacy.matcher import Matcher
from collections import Counter
import pprint
import pandas as pd 





class Document:

	def __init__(self, path):
		self.path = path
		# Loads a small/efficent web trained model
		# Medium model has vectors for word similarity/ comparisons
		self.nlp = spacy.load("en_core_web_sm")
		# Loads a Document to be analyzed
		with open (self.path, "r") as file:
			self.text = file.read()
		# Creates spacy Doc object
		self.doc = self.nlp(self.text)
		# Cleans Messy filename 
		self.clean_name = os.path.basename(self.path)
		# Default 326 stop words in spacy
		self.all_stopwords = self.nlp.Defaults.stop_words
		self.max_results = 100
		# Default include nounss in search
		self.default_phrase_speech = ''
		self.meaningful_words= []
		

	def __repr__(self):
		rep = self.clean_name
		return rep

	def get_doc(self):
		return self.doc
		
	# Takes input of string and outputs list of entire sentences  
	def sentence(self, word):
		sentence_list = []
		matcher = Matcher(self.nlp.vocab)
		pattern = [{ "TEXT": word }]
		matcher.add("Getting token",[pattern])
		match = matcher(self.doc)
		for m in match:
			sentence_list.append(self.doc[m[1]].sent)
		return sentence_list



	# Crops sentences down to under 40 words
	# Takes input of keyword string and outputs list of sentences  
	def sentence_cropped(self, word):
		sentence_list = []
		matcher = Matcher(self.nlp.vocab)
		pattern = [{ "TEXT": word }]
		matcher.add("Getting token",[pattern])
		match = matcher(self.doc)
		
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
					print(span)
					sentence_list.append("..." + span.text )

		return sentence_list





	# Takes  a list of strings as desired new stop words as input
	def add_stop(self, list_new_stops):
		if type(list_new_stops) == list:
			for stop in list_new_stops:
				self.all_stopwords.add(stop)


	# Sets max number of results to be shown
	def set_number_results(self, results):
		if type(results) == int:
			self.max_results = results
	


	# Inlude other phrases of speech as important
	# Pass'N' to include Nouns , 'A' for Adjectives 'V' for Verbs
	# Pass empty string for no additional phrases to be included
	def set_default_phrases(self, NVA):
		if type(NVA) == str and len(NVA) < 4:
			upper = NVA.upper()
			self.default_phrase_speech = upper




	# Makes a list of Interesting words (Essentially all Pronouns)
	# This includes Locations, Countries, Orgs, Events, Persons
	def interesting_entities(self):	
		doc = self.doc
		interesting = []

		# Filter out dates, numbers out of important entities
		filter_ent = ["CARDINAL" , "ORDINAL" , "DATE", "PERCENT", "MONEY", "QUANTITY"]
		
		# Splits multi word entities into single words
		for ent in doc.ents:
			if " " in ent.text:
				s = ent.text
				split_entity = s.split(" ")
				for e in split_entity:
					if ent.label_ not in filter_ent:
						interesting.append(e)			
			else:
				if ent.label_ not in filter_ent:
					interesting.append(ent.text)
			# print(ent.label_)	#show the type of entity 	
		self.meaningful_words += interesting
		return interesting	




	# Using Matcher to find nouns, verbs, adjective
	# Can later implement patterns e.g. : An Adj directly followed by noun
	# Filters out stop words
	def additional_interest(self):
		doc = self.doc
		list_patterns = []
		more_interesting = []
		if self.default_phrase_speech == "":
			return []
		if "N" in self.default_phrase_speech :
			list_patterns.append({"POS":"NOUN"})
		if "V" in self.default_phrase_speech :
			list_patterns.append({"POS":"VERB"})
		if "A" in self.default_phrase_speech :
			list_patterns.append({"POS":"ADJ"})
		'''
		list_patterns = [{"POS":"NOUN"}]
		#list_patterns = [{"POS":"NOUN"}, {"POS":"VERB"}, {"POS":"ADJ"}, {"POS":"PROPN"}]
		'''
		for pattern in list_patterns:
			matcher = Matcher(self.nlp.vocab)
			matcher.add("OtherInteresting",[[pattern]])
			match = matcher(doc)
			#print(len(match))
			for m in match:
				#print(m) # Outputs (lexeme, start token, end token)
				#print(doc[m[1]:m[2]]) # Access the text of token
				more_interesting.append(doc[m[1]:m[2]].text)	
		
		filtered_list = (list(tok for tok in more_interesting if not tok in self.all_stopwords))
		self.meaningful_words += filtered_list
		return filtered_list





	# Show frequency of all words in the document
	def output_all_freq(self):
		t = [tok.text for tok in self.doc if tok.is_punct != True]
		frequency = Counter(t)
		top_common = frequency.most_common(20)
		print(len(top_common))
		pprint.pprint(top_common)
		return top_common
	



	# Show frequency of all words in the document
	# Returns a dataframe
	def output_targetted(self):
		t = [tok.text for tok in self.doc if tok.is_punct != True and tok.is_stop != True and tok.text in self.meaningful_words ]
		frequency = Counter(t)
		top_common = frequency.most_common(self.max_results) # Returns a tuple ("Keyword", Frequency)
		
		# Colummns Word(Frequency), Document Name, Relevant sentence
		w = []
		d = []
		s = []
		for i, top_word in enumerate(top_common):
			#
			for occurance in self.sentence_cropped(top_word[0]):
				w.append(top_word[0] + f" ({str(top_word[1])})")
				occurance = occurance.replace('\n', ' ')
				occurance = occurance.replace('\t', ' ')
				s.append(occurance)
				d.append(self.clean_name)

		df = pd.DataFrame({"Word (Frequency)": w,"Document Name": d,"Sentence": s })
		return df
 



















