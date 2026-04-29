import pdfplumber
import csv
import re

# source pdfs are found at: https://www.tanos.co.uk/jlpt/jlpt5/

def containsJapanese(text):
    # regex covers Hiragana, Katakana, and common Kanji ranges
    pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]')
    return bool(pattern.search(str(text)))

def split_synonyms(text):
    if not text:
        return []

    pattern = r'[、/]+'
    
    # re.split returns a list
    parts = re.split(pattern, text)
    
    # clean up strip whitespace and remove empty strings
    return [p.strip() for p in parts if p.strip()]

def vocabPdfParseNoCleanup(pdf_path, output_csv):
    extracted_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            
            if table:
                for row in table:  

                    # skip header row
                    if not row or row[0] == "Kanji":
                        continue
             
                    # pdf format is unreliable 
                    # kanjis are found on index 0 and 1
                    kanji = next((row[i].strip() for i in [1, 0] if row[i]), "")

                    # reading if found on columns 4, 5, 3
                    reading = next((row[i].strip() for i in [4, 5, 3] if row[i]), "")

                    if not kanji:
                        kanji = reading
                    
                    if kanji and reading:
                        extracted_data.append([kanji, reading])

                    # final check if no word is found. (skips translations)
                    if not kanji and not reading:
                        if any(containsJapanese(cell) for cell in row if cell):
                                print(f"Irregular index for words! Skipped: {row}")

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Kanji", "Reading"]) # Header
        writer.writerows(extracted_data)

    print(f"Successfully extracted {len(extracted_data)} entries to {output_csv}")    

def vocabCleanParseAnkiPdf(pdf_path, output_csv):
    extracted_data = []
    # catches ・する entries
    cleanup_pattern = r'[・.]?\s*する\s*$'

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            
            if table:
                for row in table:  

                    # skip header row
                    if not row or row[0] == "Kanji":
                        continue
             
                    # pdf format is unreliable therefore the indexes vary 
                    kanji = next((row[i].strip() for i in [1, 0] if row[i]), "")
                    reading = next((row[i].strip() for i in [4, 5, 3] if row[i]), "")

                    if not kanji:
                        kanji = reading
                    
                    if kanji and reading:
                        kanji = re.sub(cleanup_pattern, '', kanji).strip()
                        reading = re.sub(cleanup_pattern, '', reading).strip()

                        splitKanji = split_synonyms(kanji)
                        splitReading = split_synonyms(reading)
                        
                        for entry in splitKanji:
                            for readingEntry in splitReading:
                                extracted_data.append([entry, readingEntry])

                    # final check if no word is found. (skips translations)
                    if not kanji and not reading:
                        if any(containsJapanese(cell) for cell in row if cell):
                                print(f"Irregular index for words! Skipped: {row}")

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Kanji", "Reading"]) # Header
        writer.writerows(extracted_data)

    print(f"Successfully extracted {len(extracted_data)} entries to {output_csv}")

def kanjiPdfParse(pdf_path, output_csv): 
    extracted_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            
            if table:
                for row in table:  
                    if not row or row[0] == "Kanji":
                        continue
                    kanji = next((row[i].strip() for i in [0, 1] if row[i]), "")
                    if (kanji and len(kanji) == 1):
                        extracted_data.append(kanji)
                        continue
    print(extracted_data)

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Kanji"])
        writer.writerows(extracted_data)

    print(f"Successfully extracted {len(extracted_data)} entries to {output_csv}")

for jlptLevel in range(1, 6):
    print(f"Parsing VocabList.N{jlptLevel}.pdf...")
    vocabPdfParseNoCleanup(f"data/rawData/VocabList.N{jlptLevel}.pdf", f"data/vocab/parseNoCleanup/n{jlptLevel}_vocab.csv")
    vocabCleanParseAnkiPdf(f"data/rawData/VocabList.N{jlptLevel}.pdf", f"data/vocab/parsedData/n{jlptLevel}_vocab_cleaned.csv")
    kanjiPdfParse(f"data/rawData/KanjiList.N{jlptLevel}.pdf", f"data/kanji/parsedData/n{jlptLevel}_kanji.csv")