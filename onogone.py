from structure import urlForumBoard

#url       = 'http://www.jeuxvideo.com/forums/42-68-58784902-1-0-1-0-les-temps-changent.htm'
url       = 'http://www.jeuxvideo.com/forums/42-51-58723294-3-0-1-0-qui-est-bon-en-ski-ici.htm'
filename  = 'testMessages.json'
dico      = 'dictionnaire.xml'
fileCorr  = 'correctedMessages.json'

object    = urlForumBoard()
boardMess = object.extractMessages(url)
object.writeFile(filename,boardMess)
messages  = object.readJson(filename)
#dict      = object.loadDictionary()
okMess    = object.treatMessages(messages)
#corrMess  = object.replaceMessages(okMess,dict)
#object.writeFile(fileCorr,corrMess)