# Goodreads Study
I want to explore the value of the genre shelf lists on Goodreads, and **more specifically the non-fiction books**.

## What are shelves on Goodreads?

Shelves are technically based on tags that the community enters on each book. Books marked as “Psychology” will end up in the Psychology shelf. In theory, the more a book is popular, the higher the chances are that it will be marked with tags, and the higher up in the shelf list it will appear: it is ordered by the number of corresponding tag it received. The book at the top of the Psychology shelf has the highest number of user tags “Psychology”.

## About Goodreads

Goodreads is a reference in terms of book exploration, book/readings tracking, and book ratings — although its ratings is considered by some as not very reliable.

One could argue that it is hard to rate a book, as it is a subjective judgement. Additionally, Goodreads being owned by the company Amazon, we can consider the potential financial incentives that would push the company in controlling the ratings and reviews of certain books.

**An interesting shelf in Goodreads is called “DNF”: Did Not Finish.** It is an “official” shelf listing books tagged as DNF by users. Namely, we have a list of books that users gave up on reading. We can’t say for sure if this list is 100% correct, as Goodreads/Amazon owns this data and can change it at will. But it is still a good indication of if a book would be, actually, not so good: one does not give up reading an interesting book.

With this in mind, we will look at the data from the non-fiction and DNF shelves in Goodreads.

## Technical Infos

This project is written in Python, using Pandas. The charts are created with Seaborn.

In order to get data from Goodreads, I created a webscraper. For this, I use Selenium and BeautifulSoup.

## Data insights

### How many of the non-fiction shelved books are also present at the top of the DNF shelf?

![books_in_dnf.png](https://github.com/eugsa/goodread_study/blob/main/figures/books_in_dnf.png)

In this graph, we can see that from the 400 books scraped in the non-fiction shelf, 50 are also present in the DNF shelf, which is 12.5%. It’s not too bad! Especially knowing that the DNF data contains 1250 books (the 1250 most tagged books with “DNF”).

### How does the ranking from the non-fiction and DNF shelves compare? For example, could it be that the most popular books are actually the least finished?

![tag_ranking.png](https://github.com/eugsa/goodread_study/blob/main/figures/tag_ranking.png)

The data scraped from the shelves is ordered by the number of tags for that given category: the first book in the DNF shelf is the book with the most DNF tag count, the highest number of users tagging the book as DNF.

Non-fiction ranking goes that way:

- The closer the index is to 0, the more popular and known the book it, potentially also loved and praised.
- The further away, the less the book is known or popular.

The DNF ranking goes as follow:

- The closer the index is to 0, the least finished the book was; and we could interpret it as the most disliked.
- The further away: potentially more people managed to read and appreciate the book.

What we can see from this figure is that most of the dots are concentrated in the bottom part of the graph. Which suggests that there might be a tendency for the highest ranked books in the non-fiction shelf to end up in the DNF shelf too.

In a sense, the fault might not be on the books themselves: the more popular the books are, the more exposed they are to masses, and thus more exposed to criticism or potentially ending up in the hands of the wrong audience.

What is interesting is also this white space on the top left side, which suggests that the lesser known non-fiction books are, they might either be judged less harshly by the readers, or maybe end up in the hands of the right audience, who would have learned from the book from quality recommendation.

[WIP]