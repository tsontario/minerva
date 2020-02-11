**Purpose:** Provide suggestions of corrected words to the user.

**Input:** Query

**Output:** Suggestion for a different query (if applicable). "Did you mean X? "

**Requirements and challenges:**
Can make it such that when typing the query, the spelling correction suggestions are displayed and are able to be selected.

Or can make it such that the search is made with the given query, but the results will display that the spelling correction has been corrected from their misspelled input to the found word. For example, if the word ‘cmputr’ yields no results when searching, you can detect that they likely meant ‘computer’ and switch the query value. Then the user would be alerted of the query change with the returned results and will be able to re-submit with the original query (something like ‘Continue search with cmputr’ as an option). Ensure that the weighted edit distance calculation is performed rapidly, especially if the dictionary is quite large and the input query must be compared to all words. The weight choice for the weighted edit distance is to be selected by you.

An example of weighted edit distance is to have a lesser cost on particular characters (such as vowels or letters that are close by on keyboards). There are many different ways to implement the weighting portion of the algorithm. You can use some heuristics, such as the fact that people very rarely get the first letter wrong, so you can limit the search to the dictionary words starting with the same word.

There might be more than one candidate word for the correction. You should show the top N most likely candidates. For likeliness, you could use their frequency in the corpus.

**Modules depending on this module:** UI and perhaps others based on design.

**Modules required by this module:** Dictionary building.
