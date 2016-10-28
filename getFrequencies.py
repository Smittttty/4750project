testFile = file("sampleText.txt", "r")
word1 = None
word2 = None
word3 = None
frequencies = dict()
for line in testFile:
    for word in line.split():
        #convert to lower case
        word = word.lower()
        #remove punctuation
        word = filter(lambda ch: ch not in ",.()\'\"!?[]{}_-+=/<>|\\~`@#$%^&*;:", word)
        if word1 == None:
            word1 = word
        elif word2 == None:
            word2 = word
        elif word3 == None:
            word3 = word
        else:
            word1 = word2
            word2 = word3
            word3 = word
        if word3 != None:
            tup = (word1, word2, word3)
            if tup not in frequencies:
                frequencies[tup] = 1
            else:
                frequencies[tup] += 1

for key in frequencies:
    print (str(key) + " " + str(frequencies[key]))
