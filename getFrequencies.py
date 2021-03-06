import cPickle
import collections
import os
import string
from Tkinter import END
from Tkinter import Entry
from Tkinter import IntVar
from Tkinter import Label
from Tkinter import OptionMenu
from Tkinter import StringVar
from Tkinter import Tk
from Tkinter import RIGHT

# noinspection PyUnusedLocal
def load_n_gram_dict(*args):
    """sets the current nGram to the one defined in the options

    :param args: where the function was triggered (not used)
    :return: nothing
    """
    # convert the choices into the proper path and load the nGram associated with it
    global nGram
    n_gram_file_name = fileName.get() + "_{0}.ng".format(size.get() + 1)
    n_gram_path = os.path.join("text_sources", n_gram_file_name)
    nGram = cPickle.load(open(n_gram_path, "rb"))


def generate_ngram_string(n, input_str, ngram=None):
    """Create an n-gram frequency dictionary based on the data in the file.

    :param n: the size of the desired n-grams
    :param input_str: the string we want to analyze
    :param ngram: the dictionary to be appended to (defaults to {})
    :return: a dictionary that encodes frequencies of different n-grams
    """
    # open the file
    if ngram is None:
        ngram = {}

    # start a deque to store the words
    word_deque = collections.deque(maxlen=n - 1)
    # run through each line in input_str
    for line in input_str.split("\n"):
        # and each word in the line
        for word in line.split():
            # convert to lower case
            word = word.lower()
            # remove punctuation and non ASCII characters
            printable = set(string.printable)
            word = filter(lambda ch: ch not in ",.()'\"!?[]{}_-+=/<>|\\~`@#$%^&*;:" and ch in printable, word)
            # check if n-1 words are in the deque

            if len(word_deque) == n - 1:
                # if so, check if the deque is a key in the dictionary, if not create a dictionary as its value
                tup = tuple(word_deque)
                if tup not in ngram:
                    ngram[tup] = {}
                # then check if the inner dictionary has the next word as a key, if not, initialize it
                if word not in ngram[tup]:
                    ngram[tup][word] = 1
                # increase the count and pop out the left-most (oldest) word
                ngram[tup][word] += 1
                word_deque.popleft()
            # add the new word to the deque
            word_deque.append(word)
    # return the n-gram dictionary
    return ngram


def get_best_m_matches(n_gram, m, inputted_words):
    """Finds the most frequent m matches in a given n-gram dictionary based on the argument.

    :param n_gram: the n-gram dictionary to be checked against
    :param m: the number of matches required
    :param inputted_words: the words to be compared against the n-gram dictionary
    :return: a list of the m most common words after the given input (returns None if no matches are found)
    """
    # only consider the last $size words
    tup = tuple(inputted_words[-size.get():])
    # if those words are in the dictionary, get the best m of them and return them as a list
    if tup in n_gram:
        words = n_gram[tup]
        sorted_words = sorted(words, words.get)
        return sorted_words[0:m]
    return None


# noinspection PyUnusedLocal
def match_entry(*args):
    """Sets the result labels to the result of finding the best 6 matches based on the matchThis input box.

    :param args: where the function was triggered (not used)
    :return: nothing
    """
    # clear the result labels first
    for j in range(len(result)):
        result[j].set("")
    # split the input into a list and find the best 3 entries
    entry = matchThis.get().split()
    words = get_best_m_matches(nGram, 3, entry)
    # if a non-None result is return, update the label to be those words
    if words is not None:
        j = 0
        for word in words:
            result[j].set(word)
            j += 1


def insert_text(j):
    """Inserts the chosen text into the entry box

    :param j: the index of the result to be added
    :return: nothing
    """
    matchThis.insert(END, " " + result[j].get())


def convert_to_readable_format(file_name_options):
    """converts the given file name options list to a list with only the source names

    :param file_name_options: the file name options that needs to be converted
    :return: the shortened file name options list
    """
    # set up the output list
    out = []
    for option in sorted(file_name_options)[::5]:
        if option[-3:] == ".ng":
            out.append(option[:-5])

    return out


# initialize the nGram variable
nGram = {}

# set up the ui frame and give it a title
root = Tk()
root.wm_title("Text Predictor")

# set up a label prompting the user to enter text
Label(root, text="Enter text:").grid(row=0)

# set up as string variable to call the match entry function whenever it is changed
enteredText = StringVar()
enteredText.set("")
enteredText.trace("w", match_entry)

# set up the entry box for the user to enter text (using the enteredText string variable)
matchThis = Entry(root, textvariable=enteredText, justify=RIGHT)
matchThis.grid(row=0, column=1)

# set up the result string variable and the label that holds it
result = []
for i in range(3):
    result.append(StringVar())
    result[i].set("")
    label = Label(root, textvariable=result[i])
    label.grid(row=1, column=i)
    label.bind("<Button-1>", lambda e, j=i: insert_text(j))

# the n-gram size options (choice of n-1) this allows you to choose how many words the dict is keyed on
sizeOptions = [
    1,
    2,
    3,
    4,
    5
]

# set up the int variable that holds the size of n-1, and set its default value to the first option in sizeOptions
size = IntVar()
size.set(sizeOptions[0])
# set a trace on this variable that calls load_n_gram_dict on any change
size.trace("w", load_n_gram_dict)

# directory which contain texts
textDirectory = "text_sources"

# get files in directory for options
fileNameOptions = os.listdir(textDirectory)

fileNameOptions = convert_to_readable_format(fileNameOptions)

# set up the variable that holds the domain file, and set its default value to the first option in fileNameOptions
fileName = StringVar()
fileName.set(fileNameOptions[1])

# set a trace on this variable that calls load_n_gram_dict on any change
fileName.trace("w", load_n_gram_dict)

# create a new n_gram_dict based on the default size and domain
load_n_gram_dict()

# create the menu that holds the size options
sizeMenu = apply(OptionMenu, (root, size) + tuple(sizeOptions))
sizeMenu.grid(row=2, column=0)

# create the menu that holds the domain options
fileMenu = apply(OptionMenu, (root, fileName) + tuple(fileNameOptions))
fileMenu.grid(row=2, column=1)

# start the UI
root.mainloop()
