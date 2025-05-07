
def makeCSV():
    with open("data/allWords/words.csv", "w") as writeFile:
        writeFile.write(f"Word,JLPTLevel\n")
        for jlptLevel in range(1, 6):
            with open(f"data/rawData/N{jlptLevel}.txt") as file:
                for line in file:
                    writeFile.write(f"{line.strip()},N{jlptLevel}\n")
        
makeCSV()