# JLPT Vocabulary and kanji in JSON and CSV Formats
The original files from: https://www.tanos.co.uk/jlpt/ are formatted in difficult to read file structures like .anki, .mem, .doc, .pdf. 
This Project aims to provide a clean, lossless and easy format for these files.<br>

You can download the files here: <a href="https://github.com/Bluskyo/JLPT_Vocabulary/releases/latest">Latest release</a>

The project files include parsed versions of the pdf files both a raw parse with minimal manipulation of the data and a more filtered version called "..._cleaned". 
The cleaned files have a stricter filter and have had the following manual changes made:

Manual Changes:<br>
**n1_vocab_cleaned.csv:**<br>
Removed "対立,たいりつ". Reason: Already defined in N2.<br>
**n2_vocab_cleaned.csv:**<br>
Updated: "=立" to "対立". Reason: Likly a conversion bug.<br>Removed "あげる (=やる),あげる (=やる)". Reason: Doesnt fit any words that are not already defined.<br>
**n3_vocab_cleaned.csv:**<br>
Removed: "暖かい,あたたか(い)" Reason: Already defined in N5.

## NOTE: 
With the new structuring of the data it is now possible to check the reading of the word.
Problems with entries such as "年" where it can have the reading as  "とし", "ねん", "とせ". Not to mention all the readings for 生...

Kanji and readings with multiple levels are preserved: JLPT_vocab_ALL.json structure<br>
```
    "挨拶": [
        {
            "reading": "あいさつ",
            "level": 3
        }
    ],
    "あいさつ": [
        {
            "reading": "あいさつ",
            "level": 4
        }
    ],

```
JLPT_kanji_ALL.json structure<br>
```
"気": 5,
```
