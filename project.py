import json 
import time

def main():
    global syllablesdata #creates a global variable for syllables data but doesn't assign yet
    global thesaurusdata #creates a global variable for thesaurus data but doesn't assign yet
    print("Please wait while the program loads and sorts the thesaurus in alphabetical order.")
    start = time.time()
    thesaurusdata = load_jsonl("en_thesaurus.jsonl") #passes in the thesauraus jsonl filename to load_jsonl
    #this now is a sorted list of json elements in alphabetical order of word that's being looked up to find synonyms of.
    end = time.time()
    print("Total time taken: "+str(end-start)) #outputs time it took to sort the entire thesauraus.
    print("Welcome! This program takes in a file you specify and outputs the readability of it. This follows the Flesch Reading Ease index that corresponds to a US grade level.")
    print("In order to start, make sure the file you're inputting is something that is an actual form of content (an essay, book, poem, etc.) as this program is designed to output readability based off of certain things found in content formats.") 
    print("For the convenience of this project, I've included three tester .txt files in the folder: omelas.txt, tofeelwhatialwayssee.txt and rotk.txt.")
    print("The first is an essay I wrote in grade 9 about a utopia, the second is a poem I wrote last year for school, and the third is a tester file that was provided in the lectures.")
    syllablesdata = loadsyllablesdata()
    #syllablesdata now has any syllable data from a file of words previously calculated in this program.
    
    continueprogram = True
    #allows the user to continue inputting files to calculate for.
    while continueprogram == True: 
        synonyms = {} #this will store all data for synonyms
        filedata = {} #this stores all file data
        originaltotalsyllables = 0
        maximizetotalsyllables = 0
        minimizetotalsyllables = 0
        fileinvalid = True 
        #checks to see if the user inputs a file with the correct extension, and allows them to keep inputting until they input a correct one.
        while fileinvalid == True:
            print("--------------------------------------------------------------------------")
            filename = input("Enter the name of the file that you want processed. Please note we can only handle .txt files at this time: ")
            if filename.endswith(".txt"):
                fileinvalid = False
            else:
                print("Error. You're trying to input a file that doesn't have a .txt extension.\n")
        print("--------------------------------------------------------------------------")
        
        uneditedwords, sentencecount = load(filename) #Returns list of words from the content of the file and the total sentence count.
        editedwords = editwords(uneditedwords) #Takes unedited words list from previous line and returns the words without any symbols or punctuations.

        start = time.time()
        #o(n) with n being the number of words in the text.
        for word in editedwords: 
            syllablescheck(word)#this passes the word into the function syllablescheck
            #syllablescheck adds the word and the amount of syllables to the dictionary syllablesdata.
            originaltotalsyllables += syllablesdata[word.lower()]
            #adds the number of syllables for the word to a cumulative total of all syllables in the text.
            if word in synonyms: #checks if the word is a key in the dictionary synonyms.
                synonyms[word.lower()][2] += 1 #index 2 represents frequency of the word in the text. This increases the frequency of the word by 1.
            else:
                synonyms[word.lower()] = synonymchecker(word.lower())
                #returns a 2d list that should look like [[smallestsynonym, syllables(0)], [biggestsynonym, syllables(0)], frequency(1)] and stores that as the value for the word in the dictionary.
        end = time.time()
        print("Total time taken to calculate syllables and find synonyms: "+str(end-start)+".")
        #Outputs the amount of time it took to calculate syllables for the words in the original text (not the synonyms), and to find the smallest and largest synonyms for each word.
        score = fleschreadingeasetest(len(editedwords), sentencecount, originaltotalsyllables) #passes three values in that are used to calculate the score for the readability test.
        
        filedata["filename"] = filename
        filedata["sentencecount"] = sentencecount
        filedata["wordcount"] = len(editedwords)
        filedata["syllablecount"] = originaltotalsyllables
        filedata["fleshreadingeasetestindex"] = score
        #saves these values all in a dictionary called filedata.
        #Originally, an extension was going to be saving all of this data into a file for a user to look back on, but I never got to it.

        #this Boolean value and while loop allows the user to keep choosing between maximize the readability or minimize until they want to quit.
        maxmincontinue = True
        while maxmincontinue:
            print("--------------------------------------------------------------------------")
            print("This program finds synonyms for words in the text in order to minimize or maximize your readability.")
            print("To 'maximize' means to make the text easier to read, and to 'minimize' means to make it more complex.\n")
            print("1: 'maximize'")
            print("2: 'minimize'")
            print("Type in anything else to skip minimizing or maximizing the readability.\n")
            option = input("Please indicate which option you prefer: ")
            print("--------------------------------------------------------------------------")

            
            if option.lower().strip() in ["1", "maximize","max", "1:"]: #The in operator has an O(n) complexity.
                if "maxscore" in filedata: #checks if the maximum readability score was already calculated and reoutputs the grade level.
                    print("\nYou've already outputted this. The new score for the data was: " + str(filedata["maxscore"])+".")
                    print("What does this score mean?")
                    fleschreadingscorehelper(filedata["maxscore"])
                else:
                    option = "max" 
                    synonyms, maximizesyllablecount = maximize(synonyms) #feeds the synonyms dictionary into the function maximize.
                    #returns the synonyms dictionary, but this time with syllable calculations for all of the simpler synonyms.
                    #also returns a total syllable count for the next text with the simpler synonyms.
                    filedata["maximizesyllablecount"] = maximizesyllablecount
                    newtext = outputtedresults(replace(option, uneditedwords, editedwords, synonyms))
                    #first calls on the function replace and feeds it the user option, both the uneditedwords and editedwords list, and the synonyms dictionary.
                    #this returns a list of words that have been replaced with the synonyms, with all the punctuation and capitalization intact of the original text.
                    #then it feeds that into outputtedresults, which concatenates each word with spaces into a single string and returns it.
                    print("Here's the output: \n")
                    print(newtext) #prints the generated output
                    print("--------------------------------------------------------------------------")
                    print("You chose to maximize the readability of your piece. Each word in your text was checked to see if there was a less complex synonym that could replace it.Here are the stats for the output: \n")
                    newscore = fleschreadingeasetest(newtext.count(" ")+1, sentencecount, maximizesyllablecount) #calculates the new score for the text and outputs grade level.
                    #there's an updated word count due to the fact that some synonyms are phrases of two or more words, hence the count of spaces for wordcount.
                    filedata["maxscore"] = newscore

            elif option.lower().strip() in ["2", "minimize", "min", "2:"]:
                if "minscore" in filedata: #checks if the minimum readability score was already calculated and reoutputs the grade level.
                    print("\nYou've already outputted this. The new score for the data was: " + str(filedata["minscore"])+".")
                    print("What does this score mean?")
                    fleschreadingscorehelper(filedata["minscore"])
                else:
                    option = "min"
                    synonyms, minimizesyllablecount = minimize(synonyms) #feeds the synonyms dictionary into the function minimize.
                    #returns the synonyms dictionary, but this time with syllable calculations for all of the more complex synonyms.
                    #also returns a total syllable count for the next text with the more complex synonyms.
                    filedata["minimizesyllablecount"] = minimizesyllablecount
                    newtext = outputtedresults(replace(option, uneditedwords, editedwords, synonyms))
                    #first calls on the function replace and feeds it the user option, both the uneditedwords and editedwords list, and the synonyms dictionary.
                    #this returns a list of words that have been replaced with the synonyms, with all the punctuation and capitalization intact of the original text.
                    #then it feeds that into outputtedresults, which concatenates each word with spaces into a single string and returns it.
                    print("Here's the output: \n")
                    print(newtext) #prints the generated output
                    print("--------------------------------------------------------------------------")
                    print("You chose to minimize the readability of your piece. Each word in your text was checked to see if there was a more complex synonym that could replace it. Here are the stats for the output: \n")
                    newscore = fleschreadingeasetest(newtext.count(" ")+1, sentencecount, minimizesyllablecount) #calculates the new score for the text and outputs grade level.
                    #there's an updated word count due to the fact that some synonyms are phrases of two or more words, hence the count of spaces for wordcount.
                    filedata["minscore"] = newscore
            else:
                maxmincontinue = False
                #if the user does not submit a valid option, this while loop quits.

        choice = input("\nWould you like to input another text file to be read? Type 'yes' to input another file, and anything else to quit: ")
        #asks the user if they want to input another file
        if choice.lower().strip() != "yes":
            continueprogram = False
            savesyllablesdata()
        #if they don't answer "yes", changes the boolean value to False to quit the while loop and calls on savesyllabledata() to save the syllable dictionary to file.
            

def load(filename):
    #opens file specified by user and reads it.
    #calls on sentences() function in order to get the sentence count of the text.
    #splits the text into a list of unedited words (including punctuation, symbols, etc.)
    #returns the list of unedited words and the number of sentences.
    filein = open(filename, "r")
    uneditedcontent = filein.read()
    numberofsentences = sentences(uneditedcontent) #returns number of sentences
    filein.close()
    return uneditedcontent.split(), numberofsentences

def load_jsonl(filename):
    #loads the thesaurus jsonl file.
    #parses through every line in the file and appends the line to a list.
    #each element in this list represents a json that contains a word and its synonyms.
    #calls on thesaurusmergesort(), a function designed to specifically alphabetically sort the jsons by the words we're going to be searching for to find synonyms of.
    #returns the list of jsons.
    thesaurusdata = []
    with open(filename, "r") as f:
        for line in f:
            thesaurusdata.append(json.loads(line.strip('\n|\r')))
    thesaurusdata = thesaurusmergesort(thesaurusdata)
    return thesaurusdata


def thesaurusmerge(list1, list2):
    #helper function for thesaurusmergesort()
    result = []
    while len(list1) > 0 or len(list2) > 0:
            if len(list1) == 0:
                    result.append(list2.pop(0))
            elif len(list2) == 0:
                    result.append(list1.pop(0))
            else:
                    if list1[0]["word"].lower() < list2[0]["word"].lower(): 
                            result.append(list1.pop(0))
                    else:
                            result.append(list2.pop(0))
    return result
	
def thesaurusmergesort(alist):
    #a merge sort designed to compare the values for "word" keys of every json in the list, sorting the list alphabetically.
    #this returns a sorted list.
    #recursive sorting
    if len(alist) <= 1:
            return alist
    list1 = thesaurusmergesort(alist[:int(len(alist)/2)])
    list2 = thesaurusmergesort(alist[int(len(alist)/2):])
    return thesaurusmerge(list1,list2)

def loadsyllablesdata():
    #at the start of the program, reads the syllablesdata.txt file to see if there's any previously calculated syllable data from this program.
    #reads it in and puts it in a dictionary.
    #returns the dictionary.
    syllables = {}
    file = open("syllablesdata.txt", "r")
    for line in file:
        pair = line.strip().split(",") #splits by commas due to how it's saved.
        syllables[pair[0]] = int(pair[1])
    file.close()
    return syllables

def savesyllablesdata():
    #at the end of the program, this is called to save all the calculated syllable data, old and new, to the same textfile we loaded from.
    file = open("syllablesdata.txt", "w")
    for element in syllablesdata:
        file.write(element+","+str(syllablesdata[element])+"\n") #separates key and value pairs with a comma.
    file.close()
    return

def sentences(uneditedcontent):
    #called upon within the load() function.
    #returns the amount of sentences in the text by counting main ways of ending a sentence: periods, exclamatation marks, and question marks.
    return uneditedcontent.count(".") + uneditedcontent.count("!") + uneditedcontent.count("?")

def editwords(uneditedwords):
    #edits the words to get rid of common punctuation and symbols like periods, commas, quotation marks, etc.
    #returns the list of edited words.
    editedwords = [] 
    for word in uneditedwords:
       editedwords.append(word.strip(' ["-;:,./()-?!\%]+')) #.lower here
    return editedwords

def syllablescheck(word):
    #this is used to find out how many syllables are in a word that's passed into it.
    #the word is first made lowercase.
    #This is not because of the original text, which passes in lowercase words to this function.
    #This is actually due to the fact that some synonyms that need their syllables calculated have need for capital letters (i.e. name of months)
    #Checks if the word is in the syllablesdata dictionary. If not, calls on the syllableshelper() function to calculate syllables for the word and stores it in the dictionary.
    #returns the value stored in the dictionary for the word.
    word = word.lower()
    if word not in syllablesdata:
        syllablesdata[word] = syllableshelper(word) 
    return syllablesdata[word]

def syllableshelper(word):
    #this is where the actual syllable calculation happens.
    #uses vowels to count syllables, but makes sure not to count consecutive vowels as more than one.
    vowels = ["a","e","i","o","u", "y"] 
    syllablecount = 0
    previousvowel = False
    if len(word) <= 2: #if the length of the word is less than or equal to 2, returns 1 as the syllable count.
        return 1
    else:
        if word[-1] == "e": #if the word ends with "e", remove the last letter. This is because that vowel doesn't usually make an extra syllable.
            word = word[:-1]
            
    for character in word: #iterates over the character in the word
        if character in vowels and previousvowel == False: #adds a syllable if the previous character wasn't a vowel and this character is.
            syllablecount += 1
            previousvowel = True
        else:
            previousvowel = False #if it's not a vowel, then revert this back to False.
            
    if (word.endswith("ed") or word.endswith("es")) and word[len(word)-3] not in vowels: #endings that don't usually add a syllable despite the vowel.
        syllablecount -= 1 #subtract one if this is True
    if syllablecount <= 0: 
        return 1 #accounts for words such as "the", which have an e at the end which subtracts a syllable, but no other vowels.
    else:
        return syllablecount #if the function hasn't returned at this point, returns the syllable count for the word.

def synonymchecker(word):
    #first it calls on allsynonym() and passes in the word and an empty list. That function should return a list of synonyms for the word.
    #if no synonyms were found, then add the original word to the list.
    #if synonyms were found, then call on the mergesort() function to sort through the lengths of the words.
    #that function returns a sorted list of smallest synonyms to biggest synonyms.
    #this represents the simpler, more readable synonyms to the complex, less readable synonyms.
    #returns a 2d list with the synonym with the smallest length and the synonym with the greatest length, along with a third element representing frequency of the word.
    synonymlist = allsynonyms(word)
    if len(synonymlist) == 0:
        synonymlist.append(word)
    else:
        synonymlist = mergesort(synonymlist)
    return[[synonymlist[0], 0],[synonymlist[len(synonymlist)-1], 0], 1]

def allsynonyms(word):
    #a helper function for synonymchecker() that finds the synonyms for the words passed in.
    #many consecutive elements in this sorted list of jsons can have the same word for the "word" key.
    #this is due to the fact that the same words can have different contexts and therefore different synonyms.
    #first calls findstart() to find the first occurence of the word in the list and stores it as the starting index.
    #makes a for loop in range of that startingindex to the end of the json list and checks if the element after it is the same as the word.
    #if it is, then it adds those synonyms to the list of synonyms as well.
    #if not, it returns the list of synonyms.
    #if it hasn't returned, it checks if the word has the ending "es", "'s" or "s" and calls the function again without the ending. This is due to plural words.
    #If all conditionals are exhausted, it returns an empty list.
    synonymlist = []
    startingindex = findstart(word)
    if startingindex != None:
        for i in range(startingindex, len(thesaurusdata)):
            if thesaurusdata[i]["word"].lower() == word:
                synonymlist = synonymlist + thesaurusdata[i]["synonyms"]
                if i == len(thesaurusdata)-1:
                    return synonymlist
                elif thesaurusdata[i]["word"].lower() != thesaurusdata[i+1]["word"].lower():
                    return synonymlist
            
    if word.endswith("es") or word.endswith("'s"):
         word = word[:len(word)-2]
         synonymlist = allsynonyms(word)
    elif word.endswith("s"):
        word = word[:len(word)-1]
        synonymlist = allsynonyms(word)   
    return synonymlist

def findstart(value):
    #this is a modified binary search algorithm that compares the values for "word" in the elements of thesaurusdata to the word we're trying to find synonyms for.
    #this is modified to look for the first occurance of the word, and returns the first index it finds that has the word as the value for the key "word".
    #if no value for "word" matches the word passed into this function, it returns None.
    start = 0
    end = len(thesaurusdata)-1
    
    while start <= end:
            midindex = int((start + end ) / 2)
            midvalue = thesaurusdata[midindex]["word"].lower()
            if midvalue == value:
                if midindex == 0:
                    return midindex
                elif thesaurusdata[midindex-1]["word"].lower() != value:
                    return midindex
            if midvalue < value:
                    start = midindex + 1
            if midvalue > value or midvalue == value:
                    end = midindex - 1  
    return

def merge(list1, list2):
    #mergesort() helper function
    result = []
    while len(list1) > 0 or len(list2) > 0:
            if len(list1) == 0:
                    result.append(list2.pop(0))
            elif len(list2) == 0:
                    result.append(list1.pop(0))
            else:
                    if len(list1[0]) < len(list2[0]): #sorts by length of element (length of synonym)
                            result.append(list1.pop(0))
                    else:
                            result.append(list2.pop(0))
    return result
	
def mergesort(alist):
    #called on by synonymchecker() to sort all of the synonyms by length found for the word.
    if len(alist) <= 1:
            return alist
    list1 = mergesort(alist[:int(len(alist)/2)])
    list2 = mergesort(alist[int(len(alist)/2):])
    return merge(list1,list2)   


def fleschreadingeasetest(totalwords, totalsentences, totalsyllables):
    #takes in arguments representing the word count of the text, the sentence count of the text, and the syllables count of the text.
    #calculates the score based off the passed in values and the Flesch-Kincaid formula.
    #prints the stats for the text, and then the score.
    #calls on the helper function to let the user know what the score means.
    score = 206.835 - (1.015 * (float(totalwords/totalsentences))) - (84.6 * (float(totalsyllables/totalwords)))
    print("Total Words: " +str(totalwords))
    print("Total Sentences: " +str(totalsentences))
    print("Total Syllables: " +str(totalsyllables))
    print("Flesch Reading-Ease Index Score: "+str(score))
    fleschreadingscorehelper(score)
    return score

def fleschreadingscorehelper(score):
    #helper function for fleschreadingeasetest() that lets the user know what the calculated score means in terms of grade and complexity.
    if score >= 90:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a 5th grade reading level.")
        print("This suggests that the average 11-year-old will easily comprehend the piece.")
    elif score >= 80:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a 6th grade reading level.")
        print("This suggests the piece is easy to read. It has the same effect as conversational English.")
    elif score >= 70:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a 7th grade reading level.")
        print("This suggests that the material is fairly easy to read.")
    elif score >= 60:
        print("\nAccording to the Flesch Reading-Ease Test, the material has around an 8th and 9th grade reading level.")
        print("This suggests the material is written in plain English. It's easily understood by students entering high school.")
    elif score >= 50:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a 10th to 12th reading level.")
        print("This suggests that the material is fairly difficult to read.")
    elif score >= 30:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a college reading level.")
        print("This suggests that the material is difficult to read.")
    elif score >= 10:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a college graduate reading level.")
        print("This suggests that the reader will need to have completed secondary education as the material is very difficult to read.")
    else:
        print("\nAccording to the Flesch Reading-Ease Test, the material has a professional reading level.")
        print("This suggests that the material is extremely difficult to read, making the target audience university graduates or professionals.")

def minimize(synonymsdictionary):
    #this function is called upon when the user chooses to minimize the readability of their text.
    #recall that the synonyms dictionary stores a word as a key and then the synonyms in this format:
    #synonyms[word] = [[simplestsynonym, syllablecount], [complexsynonym, syllablecount], frequencyofwordintext]
    #the complexsynonym is passed into syllablescheck() to get the syllable count.
    #checks if the syllable count for the complexsynonym is higher than the original word.
    #if yes, then updates the dictionary's syllable count for complexsynonym from 0.
    #if not, then replaces the complexsynonym with the original word and the syllable count with the original word's syllablecount.
    #adds the syllable count for whatever word is now in the dictionary in that position multiplied by the frequency of the original word to be replaced to the total syllable count.
    #returns the synonyms dictionary back and the total syllable count for the new text.
    totalsyllablecount = 0 
    for word in synonymsdictionary:
        synonymsyllablecount = syllablescheck(synonymsdictionary[word][1][0])
        if synonymsyllablecount > syllablesdata[word]:
            synonymsdictionary[word][1][1] = synonymsyllablecount
        else:
            synonymsdictionary[word][1][0] = word
            synonymsdictionary[word][1][1] = syllablesdata[word]
        totalsyllablecount += synonymsdictionary[word][1][1] * synonymsdictionary[word][2]
    return synonymsdictionary, totalsyllablecount

def maximize(synonymsdictionary):
    #this function is called upon when the user chooses to maximize the readability of their text.
    #recall that the synonyms dictionary stores a word as a key and then the synonyms in this format:
    #synonyms[word] = [[simplestsynonym, syllablecount], [complexsynonym, syllablecount], frequencyofwordintext]
    #loops through all keys in the synonyms dictionary.
    #the simplestsynonym is passed into syllablescheck() to get the syllable count.
    #checks if the syllable count for the simplestsynonym is lower than the original word.
    #if yes, then updates the dictionary's syllable count for simplestsynonym from 0.
    #if not, then replaces the simlestsynonym with the original word and the syllable count with the original word's syllablecount.
    #adds the syllable count for whatever word is now in the dictionary in that position multiplied by the frequency of the original word to be replaced to the total syllable count.
    #returns the synonyms dictionary back and the total syllable count for the new text.
    totalsyllablecount = 0
    for word in synonymsdictionary:
        synonymsyllablecount = syllablescheck(synonymsdictionary[word][0][0])
        if synonymsyllablecount < syllablesdata[word]:
            synonymsdictionary[word][0][1] = synonymsyllablecount
        else:
            synonymsdictionary[word][0][0] = word
            synonymsdictionary[word][0][1] = syllablesdata[word] 
        totalsyllablecount += synonymsdictionary[word][0][1] * synonymsdictionary[word][2]
    return synonymsdictionary, totalsyllablecount

def replace(option, uneditedwordslist, editedwordslist, synonymsdictionary):
    #this function is called on to replace the words in the original text with the synonyms depending on the option the user picked.
    #it loops through all of the indexes from 0 to the length of the uneditedwordslist
    #at the same index number, the edited word and unedited word is the same. One just has the formatting of the original text (uneditedwordslist).
    #depending on the option, it uses the replace method on the uneditedword element with the punctuation to replace the editedword part with the simpler/complex synonym.
    #maintains capitalization by checking if the capitalize method on the editedwordslist element equals the original editedwordslist element.
    #if yes, then the synonym gets capitalized too.
    #appends the word to a new list called replacedlist.
    #once the loop is done and there are no more words to replace, returns replacedlist.
    replacedlist = []
    for i in range(len(uneditedwordslist)):
        if option == "max":
            if editedwordslist[i].capitalize() == editedwordslist[i]:
                word = uneditedwordslist[i].lower().replace(editedwordslist[i].lower(), synonymsdictionary[editedwordslist[i].lower()][0][0].capitalize())
            else:
                word = uneditedwordslist[i].lower().replace(editedwordslist[i].lower(), synonymsdictionary[editedwordslist[i].lower()][0][0])
            replacedlist.append(word)
        else:
            if editedwordslist[i].capitalize() == editedwordslist[i]:
                word = uneditedwordslist[i].lower().replace(editedwordslist[i].lower(), synonymsdictionary[editedwordslist[i].lower()][1][0].capitalize())
            else:
                word = uneditedwordslist[i].lower().replace(editedwordslist[i].lower(), synonymsdictionary[editedwordslist[i].lower()][1][0])
            replacedlist.append(word)      
    return replacedlist

def outputtedresults(content):
    #this function takes the new words list complete with synonym substitution from the replace() function and formats it into a string with spaces.
    #once all the words in the list are added to the string, returns the final output of the text.
    output = ""
    for word in content:
        if output == "":
            output = word
        else:
            output = output + " " + word
    return output

main() #calls on the main() function to begin.
