# messages_analysis
This small function allows the user to extract the messages from a forum board (here from jeuxvideo.com, although other sites may be implemented in the future) or any list of strings contained in a JSON file, and reduce each word from each message to its radical. The resulting corrected messages are returned in a JSON file.

The current routine is optimized for the *french language*, others may be added in the future. 

The file **main.py** runs the routine on a page of the jeuxvideo.com forum board and returns a JSON file containing the corrected messages for this specific thread. 

__extractMessages__ : this function extract individual messages from a jeuxvideo.com forum board URL (as input by the user). It is not necessary to run extractMessages to perform the analysis. If the user does not wish to run the routine on a jeuxvideo.com URL but on a different list of strings, they can input a filename in __readJson__ containing the list of strings and perform the analysis on the products of this routine.

__writeFile__ : this function takes a list of strings and writes them as a list of strings in a JSON file, whose name and location is defined by the user. It is used both to write the original messages from the forum board and the corrected messages after completion of the analysis.

__readJson__ : a simple function that extracts strings from a JSON file containing a list of strings.

__loadDictionary__ : this function opens and parses a dictionary located at a path defined by the user. The default dictionary is Morphalou 2.0 as found here: http://www.cnrtl.fr/lexiques/morphalou/. **Important**: due to its size, the file dictionnaire.xml containing the Morphalou 2.0 dictionary is not included in this git repository. The user should download it and add it to the same directory as the other files.

__treatMessages__ : takes strings and edits them to make them lowercase, remove contractions, correct some usual spelling errors ("J'ai" becomes "je ai", "acceuil" becomes "accueil", etc.) and split them into individual words. A wider range of spelling mistakes will be taken into account in future versions.

__replaceMessages__ : compares each word with entries of the dictionary and replaces them with their lemmatized form if applicable (infinitive form of verbs, singular form of nouns, etc.) The words that cannot be found in the dictionary (neologisms, spelling error that have not been accounted for by treatMessages, etc.) are left untouched at the moment. The function returns a list containing each individual message as a string.
