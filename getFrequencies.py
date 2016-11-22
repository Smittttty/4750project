import collections

def generateNGram(n, fileName, nGram = {}):
	testFile = file(fileName, "r")
	wordDeque = collections.deque(maxlen=n-1)
	for line in testFile:
		for word in line.split():
			#convert to lower case
			word = word.lower()
			#remove punctuation
			word = filter(lambda ch: ch not in ",.()\'\"!?[]{}_-+=/<>|\\~`@#$%^&*;:", word)

			if len(wordDeque) == 2:
				tup = tuple(wordDeque)
				if not nGram.has_key(tup):
					nGram[tup] = {}
				if not nGram[tup].has_key(word):
					nGram[tup][word] = 0
				nGram[tup][word] += 1
				wordDeque.popleft()

			wordDeque.append(word)

	return nGram

def getBestNMatches(nGram, n, *args):
	tup = tuple(args)
	if nGram.has_key(tup):
		words = nGram[tup]
		sortedWords = sorted(words, words.get)
		return sortedWords[0:n]
	return None

nGram = generateNGram(3, "sampleText.txt")

print getBestNMatches(nGram, 6, "to", "the")