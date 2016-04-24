# enbc2csv - Evernote Business Cards to CSV

A dirty little script I put together to do one thing - export business cards that have been stored in Evernote (likely using one of their card scanning apps) into a CSV file. This script is far from perfect, but I threw it together in a couple of days as I had some business cards in desperate need of liberation.

That said, if you see an error (there definitely are some known issues), or have an improvement, please feel free to submit a Pull Request. I will be happy to merge it!

## Installation

You will need [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

Once Beatiful Soup is installed into the **bs4** directory in the same directory as the script, consider enbc2csv installed.

From a Python perspective, this was coded on a Mac using Python 2.7. So, that should work. Python 3 should work as well, assuming you setup *Beautiful Soup* according to their instructions.

## Usage

Pretty straight forward:

First, export your business cards from Evernote as HTML.

Then, run the script.

```
python enbc2csv.py -i My\ Notes/*.html -o foo.csv
```

The *-i* option specifies the input file(s) that are formatted in Evernote HTML.
The *-o* option specifies the output CSV file.

Use option *-h* to see what else is available.

And, that's it! There are definitely areas for improvement with the script - but like I said, it was quick and dirty in its inception.
