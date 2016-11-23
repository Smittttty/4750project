from Tkinter import Label
from Tkinter import Tk
from Tkinter import Entry
from Tkinter import Button
from Tkinter import StringVar
from Tkinter import W
import collections

nGramSize = 4
def generateNGram(n, fileName, nGram = {}):
	testFile = file(fileName, "r")
	wordDeque = collections.deque(maxlen=n-1)
	for line in testFile:
		for word in line.split():
			#convert to lower case
			word = word.lower()
			#remove punctuation
			word = filter(lambda ch: ch not in ",.()\'\"!?[]{}_-+=/<>|\\~`@#$%^&*;:", word)

			if len(wordDeque) == (n-1):
				tup = tuple(wordDeque)
				if not nGram.has_key(tup):
					nGram[tup] = {}
				if not nGram[tup].has_key(word):
					nGram[tup][word] = 0
				nGram[tup][word] += 1
				wordDeque.popleft()

			wordDeque.append(word)

	return nGram

def getBestNMatches(nGram, n, args):
	tup = tuple(args)
	if nGram.has_key(tup):
		words = nGram[tup]
		sortedWords = sorted(words, words.get)
		return sortedWords[0:n]
	return None

def matchEntry():
    entry = matchThis.get().split()
    if len(entry) < nGramSize - 1:
        result.set("")
        return

    words =  getBestNMatches(nGram, 6, entry[-(nGramSize-1):])
    out = ""
    if(words == None):
        result.set("")
        return
    for word in words:
        out += word
        out += ", "
    out = out[:-2]
    result.set(out)

def onKeyTyped(event):
	matchEntry()

nGram = generateNGram(4, "sampleText.txt")

ui = Tk()

Label(ui, text = "Enter text:").grid(row = 0)

matchThis = Entry(ui)
matchThis.bind("<KeyRelease>", onKeyTyped)
matchThis.grid(row = 0, column = 1)

Button(ui, text = "Submit", command = matchEntry).grid(row = 3, column = 0, sticky = W, pady = 4)

result = StringVar()
result.set("")
Label(ui, textvariable = result).grid(row = 1)


#print getBestNMatches(nGram, 6, "to", "the")

ui.mainloop()