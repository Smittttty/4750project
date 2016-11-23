from Tkinter import Label, Tk, Entry, StringVar, IntVar, OptionMenu
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

			if len(wordDeque) == n - 1:
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
    tup = tuple(args[-size.get():])
    if nGram.has_key(tup):
        words = nGram[tup]
        sortedWords = sorted(words, words.get)
        return sortedWords[0:n]
    return None

def matchEntry():
    entry = matchThis.get().split()
    words = getBestNMatches(nGram, 6, entry)
    out = ""
    if words != None:
        for word in words:
            out += word
            out += ", "
        out = out[:-2]
    result.set(out)

def onKeyTyped(event):
    matchEntry()

def makeNewNGramList(*args):
    global nGram
    nGram = None
    nGram = generateNGram(size.get() + 1, fileName.get())


nGram = None

root = Tk()
root.wm_title("Text Predictor")

Label(root, text = "Enter text:").grid(row = 0)

matchThis = Entry(root)
matchThis.bind("<KeyRelease>", onKeyTyped)
matchThis.grid(row = 0, column = 1)

result = StringVar()
result.set("")
Label(root, textvariable = result).grid(row = 1)

sizeOptions = [
	1,
	2,
	3,
	4,
	5
]

size = IntVar()
size.set(sizeOptions[0])
size.trace("w", makeNewNGramList)

fileNameOptions = [
	"sampleText.txt",
	"sampleText2.txt"
]

fileName = StringVar()
fileName.set(fileNameOptions[0])
fileName.trace("w", makeNewNGramList)

makeNewNGramList()

sizeMenu = apply(OptionMenu, (root, size) + tuple(sizeOptions))
sizeMenu.grid(row = 2, column = 0)

fileMenu = apply (OptionMenu, (root, fileName) + tuple(fileNameOptions))
fileMenu.grid(row = 2, column = 1)

#print getBestNMatches(nGram, 6, "to", "the")

root.mainloop()