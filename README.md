# readability-analyzer
This project initially analyzes the readability of a text file specified by the user. It makes use of the Flesch-Reading Ease Test that uses total amounts of
syllables, word, and sentences to output an index that corresponds to a US grade level.

After the readability is analyzed and a grade level is outputted, the user is presented with the option to
either maximize the readability of the file or minimize it. To maximize the readability is to make it more
easy to read, and to minimize it to make it more complex and harder to read/understand. The user can
wish to quit if they want by inputting anything else. If the user chooses to maximize the readability, all
words in the text are searched through the contents of a thesaurus file and replaced with a simpler
synonym. If the user chooses to minimize, the words are replaced with more complex synonyms. The
Flesch-Reading Ease Test score is recalculated and outputs a grade level based off of the new text.

Thesauraus used: https://github.com/zaibacu/thesaurus
