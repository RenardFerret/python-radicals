import json
import requests
import lxml
import unicodedata
from bs4 import BeautifulSoup
from num2words import num2words

class urlForumBoard:
	'''Extracts messages from a jeuxvideo.com URL and returns the radicals of each word in a JSON file'''
	
	def extractMessages(self,url):
		'''Extract messages from URL'''
		try:
			rUrl       = requests.get(url)
		except:
			raise ValueError('This URL is not accessible!')	      
		soup       = BeautifulSoup(rUrl.text, "html.parser")
		[x.extract() for x in soup.find_all('blockquote')]
		boardMess = soup.find_all("div", {"class":"txt-msg text-enrichi-forum"})
		if boardMess == []:
			print('The class could not be found. Did you make sure you used a jeuxvideo.com URL?')
		strMess    = []   
		for mess in boardMess:
			for string in mess.stripped_strings:
				strMess.append(string)
		return strMess
		
	def writeFile(self,fileName,individualMessages):
		'''Writes list of strings in a JSON file'''
		try:
			file       = open(fileName,'w',encoding='utf-8')
			jsonFp     = json.dump(individualMessages,fp=file,indent=2,ensure_ascii=False)
			file.close()
		except:
			raise ValueError('Could not write file')
		print("The messages have been written in %s successfully." %fileName)

	def readJson(self,fileName):
		'''Reads JSON file containing the messages and returns an array with individual messages'''
		try:
			with open(fileName,'r',encoding='utf-8') as json_file:
				individualMessages = json.load(json_file,encoding='utf-8')
				print('Individual messages have been successfully loaded from %s' %fileName)
		except:
			raise ValueError("Your JSON file should be one dictionary containing strings. Use the method writeFile to get it from a jeuxvideo.com url!")
		return individualMessages

	def loadDictionary(self,dictionary='dictionnaire.xml'):
		'''Reads XML containing a dictionary (default: Morphalou 2.0)'''
		try:
			fileDico   = open(dictionary,'r',encoding="utf-8")
		except:
			raise ValueError('Unable to find dictionary')
		contents   = fileDico.read()
		soupDico   = BeautifulSoup(contents,'xml')
		print('Dictionary successfully parsed')
		return soupDico

	def treatMessages(self,individualMessages):
		'''Corrects messages for contractions and some of the usual spelling errors'''
		spellMess  = []
		initMess   = []
		if isinstance(individualMessages,list) is True:
			for message in individualMessages:
				initMess.append(message.lower())
		elif isinstance(individualMessages,str) is True:
			initMess.append(individualMessages.lower())
		else:
			print('Type is not recognized')
		for messSplit in initMess:
			### Corrections to the spelling (common mistakes)
			messSplit  = messSplit.replace("croivent","croient")
			messSplit  = messSplit.replace("ptit","petit")
			messSplit  = messSplit.replace("cauchemard","cauchemar")
			messSplit  = messSplit.replace("cauchemards","cauchemars")
			messSplit  = messSplit.replace("p'tit","petit")
			messSplit  = messSplit.replace("jsuis","je suis")
			messSplit  = messSplit.replace("parmis","parmi")
			messSplit  = messSplit.replace("malgrés","malgré")
			messSplit  = messSplit.replace("comme même","quand même")
			messSplit  = messSplit.replace("c'est","être")
			messSplit  = messSplit.replace("trés","très")
			messSplit  = messSplit.replace("tres","très")
			messSplit  = messSplit.replace("etre","être")
			messSplit  = messSplit.replace('acceuil','accueil')
			### Corrections to the contractions
			messSplit  = messSplit.replace("qu'","que ")
			messSplit  = messSplit.replace("jai","j'ai")
			messSplit  = messSplit.replace("j'","je ")
			messSplit  = messSplit.replace("t'","tu ")
			messSplit  = messSplit.replace("d'","de ")
			messSplit  = messSplit.replace("aujourde hui","aujourd'hui")
			messSplit  = messSplit.replace("l'","le ")
			messSplit  = messSplit.replace("m'","me ")
			messSplit  = messSplit.replace("n'",'ne')
			messSplit  = messSplit.split()
			if 'parce' in messSplit:
				messSplit[messSplit.index('parce')] = 'parce que'
				messSplit.pop(messSplit.index('parce que')+1)
			if 'week' in messSplit and 'end' in messSplit[messSplit.index('week')+1]:
				messSplit[messSplit.index('week')] = 'week end'
				messSplit.pop(messSplit.index('week end')+1)
			if 'soit' in messSplit and 'disant' in messSplit[messSplit.index('soit')+1]:
				messSplit[messSplit.index('soit')] = 'soi-disant'
				messSplit.pop(messSplit.index('soi-disant')+1)
			translator = str.maketrans('','','.,)?:!;"(')
			for i in range(0,len(messSplit)):
				messSplit[i] = messSplit[i].translate(translator)
				try: 
					int(messSplit[i])			
					messSplit[i] = num2words(int(messSplit[i]),lang='fr')
				except:
					pass
			spellMess.append(messSplit)
		print('Messages successfully corrected for spelling mistakes')
		return spellMess
	
	def replaceMessages(self,spellMess,dict):
		'''Takes a list containing lists of individual strings and replaces words with their radicals'''
		messagesArray = []
		for messSplit in spellMess:
			messagesSeparated = []
			for i in range(0,len(messSplit)):
				toFind = messSplit[i]
				if toFind in messagesSeparated:
					messageCorrected = messagesSeparated[messagesSeparated.index(toFind)]
				elif toFind in messSplit[:i]:
					messageCorrected = messagesSeparated[messSplit.index(toFind,0,i)]
				else:
					try:
						dictEntries  = dict.find_all(string=toFind)
						if any(dictEntry.find_parents('lemmatizedForm') != [] for dictEntry in dictEntries):
							for item in dictEntries:
								if item.find_parents('lemmatizedForm') != []:
									dictEntry = item
						elif any(dictEntry.find_parents('lexicalEntry')[0].lemmatizedForm.orthography.text == 'être' for dictEntry in dictEntries):
							for item in dictEntries:
								if item.find_parents('lexicalEntry')[0].lemmatizedForm.orthography.text == 'être':
									dictEntry = item
						else:
							dictEntry = dictEntries[0]
						if dictEntry.find_parents("lemmatizedForm") == []:
							messageCorrected = dictEntry.find_parents('lexicalEntry')[0].lemmatizedForm.orthography.text
						else:
							messageCorrected = dictEntry.find_parents('lemmatizedForm')[0].orthography.text
					except:
						messageCorrected = toFind
						print("Unable to find %s in the dictionary, leaving it as is" %toFind)
				messagesSeparated.append(messageCorrected)
			space = ' '
			messagesArray.append(space.join(messagesSeparated))		
		print('Messages successfully replaced!')
		return messagesArray
