import re
import operator
# Export the plain text of the book from: http://www.gutenberg.org/cache/epub/22764/pg22764.txt

# Open txt file and storing it in a list variable
text_lines = []
with open('Origin_of_Species.txt', 'rt') as text:
    for line in text:
        text_lines.append(line)

# From inspecting the txt file we know that the actual book text starts with 'ON THE ORIGIN OF SPECIES'
# Let's find the index of that line
start = text_lines.index('ON THE\n')

# We also know that the book text finishes just before 'End of the Project Gutenberg EBook...'
# Let's get the index of that line
end = text_lines.index('*** END OF THIS PROJECT GUTENBERG EBOOK ORIGIN OF SPECIES ***\n')

# Extract only the actual book text
book_text = text_lines[start:end]

# Drop the empty lines and the lines containing stars
star_line = '       *       *       *       *       *\n'
new_line = '\n'

while new_line in book_text:
    book_text.remove('\n')

while star_line in book_text:
    book_text.remove('       *       *       *       *       *\n')

# Strip the trailing newline
book = [re.sub('\n', '', line) for line in book_text]

# Dropping the last two lines as they actually are not part of the book
book = book[:-2]

# Eliminate all special characters except for '-' including periods
book = [re.sub('[^a-zA-Z-\d\s]', '', line) for line in book]

# Replace '-' with ' '
book = [re.sub('-', ' ', line) for line in book]

# Make everything lowercase
book = [line.lower() for line in book]

# Split each line into words
book = [line.split() for line in book]

# Create empty dictionary
d = dict()

# Create a word count in the dictionary
for line in book:
    for word in line:
        if word not in d:
            d[word] = 1
        else:
            d[word] +=1

# Create a list of key values and sort from highest to lowest
key_values = list(d.values())
sorted_values = sorted(key_values, reverse=True)

# Create list of the matching keys of the 30 most used words
top_30 = []
for i in range(30):
    top_30.append(list(d.keys())[key_values.index(sorted_values[i])])

# print(top_30)
# As the list shows these words do not give a lot of context as to what the book is about apart from the 12th
# most used word species

# Thanks to the internet there is a list of stop words that can be excluded from the word frequency
stop_words = ['could','would' ,'may',"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# Remove these stopwords from book
filtered_book = []
for line in book:
    for word in line:
        if word not in stop_words:
            filtered_book.append(word)

# Create new dictionary
new_d = dict()
for word in filtered_book:
    if word not in new_d:
        new_d[word] = 1
    else:
        new_d[word] += 1

# Create a list of key values and sort from highest to lowest
new_key_values = list(new_d.values())
new_sorted_values = sorted(new_key_values, reverse=True)

# Create list of the matching keys of the 30 most used words
new_top_30 = []
for i in range(30):
    new_top_30.append(list(new_d.keys())[new_key_values.index(new_sorted_values[i])])

# print(new_top_30)
# That looks better

# Let's put the above steps into functions so that we can look at more than single word frequencies

# Create a dictionary function
def get_dict(text):
    d = dict()
    for word in text:
        if word not in d:
            d[word] = 1
        else:
            d[word] += 1
    return d

# Create a sorted key value function
def sort_vals(text):
    d = get_dict(text)
    vals = list(d.values())
    sorted_vals = sorted(vals, reverse=True)
    return d, vals, sorted_vals

# Create a list of the n most frequently appearing keys
def top_keys(text, n):
    d, vals, sorted_vals = sort_vals(text)
    top_n = []
    for i in range(n):
        top_n.append(list(d.keys())[vals.index(sorted_vals[i])])
    return top_n

# Check to see that the functions work
# print(top_keys(filtered_book, 30))
# d, vals, sort = sort_vals(filtered_book)
# print(sort)

# Now it gets interesting
# Let's investigate the most common two word combinations from the filtered book

two_word_combo = []
for i in range(len(filtered_book) - 1):
    two_word_combo.append(filtered_book[i] + ' ' + filtered_book[i + 1])

# Check out the 30 most frequent two word combinations
# print(top_keys(two_word_combo, 30))

# Some word combinations seem to be repeating, which may be because they represent the first matching key with a
# given value. Let's see if this suspicion is true
di, va, so = sort_vals(two_word_combo)
# print(so)

# We can see that the sorted values have recurring numbers, such as 83, which means that the matching doesn't work
# the way it was constructed above.
# What is needed is a way of matching keys from a dictionary using the key value AND if a value occurs more than once
# the matching key must be selected and not simply the first one

# Function to create a reverse dictionary:
def reverse_dict(text):
    d = get_dict(text)
    rev_dict = {}
    for key, value in d.items():
        rev_dict.setdefault(value, set()).add(key)
    return rev_dict

# Function to sort keys
def sort_keys(text):
    d = reverse_dict(text)
    keys = list(d.keys())
    sort = sorted(keys, reverse=True)
    return d, keys, sort

# Function to get top n values based on sorted keys
def top_n_vals(text, n):
    d, keys, sort = sort_keys(text)
    top_n = []
    while len(top_n) < n:
        if len(sort) > n:
            for i in range(n):
                vals = list(d[list(sort)[i]])
                if len(vals) > 1:
                        for j in range(len(vals)):
                            top_n.append(vals[j])
                else:
                    top_n.append(vals[0])
        else:
            for i in range(len(sort)):
                vals = list(d[list(sort)[i]])
                if len(vals) > 1:
                    for j in range(len(vals)):
                        top_n.append(vals[j])
                else:
                    top_n.append(vals[0])
    return top_n[:n]

# Do the same with three word combinations
three_word_combo = []
for i in range(len(filtered_book) - 2):
    three_word_combo.append(filtered_book[i] + ' ' + filtered_book[i + 1] + ' ' + filtered_book[i + 2])

# Print the top 30 one, two and three word combinations
print(top_n_vals(filtered_book, 30))
print(top_n_vals(two_word_combo, 30))
print(top_n_vals(three_word_combo, 30))









