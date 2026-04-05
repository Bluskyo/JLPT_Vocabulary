import json
import csv
from collections import defaultdict

def makeCSV():
    with open("data/results/JLPTWords.csv", "w", encoding='utf8') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["Kanji", "Reading", "Level"]) # Write header

        for jlptLevel in range(1, 6):
            source_path = f"data/parsedData/n{jlptLevel}_vocab_cleaned.csv"
            
            try:
                with open(source_path, "r", encoding='utf8', newline='') as readFile:
                    reader = csv.reader(readFile)
                    next(reader) # Skip the header of the source file
                    
                    for row in reader:
                        # row is already a list, e.g., ["会う", "あう"]
                        # We just append the level and write it out
                        writer.writerow(row + [jlptLevel])
            except FileNotFoundError:
                print(f"Warning: {source_path} not found. Skipping...")
    print("Created csv file at: data/results/JLPTWords.csv")
            
def makeJSON():
    dictonary = {}
    lookup = defaultdict(list)

    for jlptLevel in range(1, 6):
        with open(f"data/parsedData/n{jlptLevel}_vocab_cleaned.csv") as file:
            next(file)
            for line in file:
                entry = line.strip().split(",")

                if entry[1] == "":
                    lookup[entry[0]].append(
                        {"reading": entry[0],
                        "level": jlptLevel}
                    )
                else:
                    lookup[entry[0]].append(
                        {"reading": entry[1],
                        "level": jlptLevel}
                    )
    
    dictonaryJson = json.dumps(lookup, indent=4, ensure_ascii=False)

    with open("data/results/JLPTWords.json", "w", encoding='utf8') as writeFile:
        writeFile.write(dictonaryJson)
    print("Created json file at: data/results/JLPTWords.json")

makeCSV()
makeJSON()