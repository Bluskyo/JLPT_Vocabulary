import json

def makeCSV():
    with open("data/allWords/JLPTWords.csv", "w") as writeFile:
        writeFile.write(f"Word,JLPTLevel\n")
        for jlptLevel in range(1, 6):
            with open(f"data/rawData/N{jlptLevel}.txt") as file:
                for line in file:
                    writeFile.write(f"{line.strip()},N{jlptLevel}\n")

def makeJSON():
    dictonary = {}

    for jlptLevel in range(1, 6):
        with open(f"data/rawData/N{jlptLevel}.txt") as file:
            for line in file:
                dictonary[line.strip()] = f"N{jlptLevel}"
    
    dictonaryJson = json.dumps(dictonary, indent=4, ensure_ascii=False)

    print(dictonaryJson)

    with open("data/allWords/JLPTWords.json", "w", encoding='utf8') as writeFile:
        writeFile.write(dictonaryJson)

##makeCSV()
##makeJSON()
