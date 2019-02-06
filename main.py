from message_analysis import urlForumBoard

url       = 'http://www.jeuxvideo.com/forums/42-68-58784902-1-0-1-0-les-temps-changent.htm'
filename  = 'testMessages.json'
dico      = 'dictionnaire.xml'
fileCorr  = 'correctedMessages.json'

object    = urlForumBoard()
boardMess = object.extractMessages(url)
object.writeFile(filename,boardMess)
messages  = object.readJson(filename)
dict      = object.loadDictionary()
okMess    = object.treatMessages(messages)
corrMess  = object.replaceMessages(okMess,dict)
object.writeFile(fileCorr,corrMess)
