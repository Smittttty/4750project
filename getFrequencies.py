import collections

#generate nGrams from file, pass in another nGram to expand on it.
def generateNGram(n, fileName, nGram = {}):
	testFile = file(fileName, "r")
	wordDeque = collections.deque(maxlen=n-1)
	for line in testFile:
		for word in line.split():
			#convert to lower case
			word = word.lower()
			#remove punctuation
			word = filter(lambda ch: ch not in ",.()\'\"!?[]{}_-+=/<>|\\~`@#$%^&*;:", word)

			#if we n-1 items in deque we add a tuple
			if len(wordDeque) == n - 1:
				#generate tuple
				tup = tuple(wordDeque)
				#create tuple key
				if not nGram.has_key(tup):
					nGram[tup] = {}
				#create word key
				if not nGram[tup].has_key(word):
					nGram[tup][word] = 0;
				#increase frequency
				nGram[tup][word] += 1;
				#remove old word from deque
				wordDeque.popleft();
			#add word to queue
			wordDeque.append(word)
	#return frequency nGram
	return nGram

#generate best n matches for nGram
def getBestNMatches(nGram, n, *args):
	#create tuple
	tup = tuple(args)
	#if we have that key
	if nGram.has_key(tup):
		words = nGram[tup]
		#sort and return best matches
		sortedWords = sorted(words, words.get)
		return sortedWords[0:n]
	return None

#test
nGram = generateNGram(3, "sampleText.txt")
#extend on old nGram
nGram = generateNGram(3, "sampleText2.txt", nGram)
#predict some words
print getBestNMatches(nGram, 3, "want", "to")
