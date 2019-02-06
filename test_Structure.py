import pytest
from structure import urlForumBoard

class TestForumBoard:
	def setup_method(self):
		self.urlOk          = 'http://www.jeuxvideo.com/forums/42-51-58723294-3-0-1-0-qui-est-bon-en-ski-ici.htm'
		self.url404         = 'http://cetteurlnexistepas.lol'
		self.urlWrongClass  = 'https://github.community/t5/Welcome/Welcome-developers-JAVA/td-p/14605'
		self.urlOneMess     = 'http://www.jeuxvideo.com/forums/42-51-58825278-1-0-1-0-ce-freestyle-d-anthologie.htm'
		self.testMessage    = ['caramba','acceuil','13',"aujourd'hui","j'ai"]
		self.testCorrection = [['plus','ai','jabberwocky']]
		self.pathDict       = 'dictionnaire.xml'
		self.wrongPath      = 'toto.xml'
		self.testFile       = 'testFile.json'
		
	def test_extractMessages(self):
		with pytest.raises(ValueError):
			errorURL = urlForumBoard().extractMessages(self.url404)
		assert urlForumBoard().extractMessages(self.urlWrongClass) == []
		assert urlForumBoard().extractMessages(self.urlOneMess)[0] == 'Bordel'
		 
	def test_readJson(self):
		with pytest.raises(ValueError):
			urlForumBoard().readJson('toto')
		assert urlForumBoard().readJson(self.testFile) == ['Success']
		
	def test_loadDictionary(self):
		with pytest.raises(ValueError):
			dict = urlForumBoard().loadDictionary(self.wrongPath)
		
	def test_treatMessages(self):
		assert urlForumBoard().treatMessages(self.testMessage) == [['caramba'],['accueil'],['treize'],["aujourd'hui"],['je','ai']]		
		assert urlForumBoard().treatMessages(87654)            == []

	def test_replaceMessages(self):
		dict     = urlForumBoard().loadDictionary(self.pathDict)
		assert urlForumBoard().replaceMessages(self.testCorrection,dict) == ['plus avoir jabberwocky']
		