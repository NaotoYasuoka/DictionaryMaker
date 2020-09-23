import os, csv
import string
import shutil
import re
import sys
sys.path.append('../')
import __init__ as init

Scores={"5":1, "4":2, "3":3, "pre2":4, "2":5, "pre1":6, "1":7}

def editScore(csv_path, adding_path, file_h, str, score):
  path = csv_path + file_h + str[0].upper() + ".csv"
  write_path = adding_path + file_h + str[0].upper() + ".csv"
  with open(path, mode="r", encoding="utf-8") as rf:
    reader = csv.reader(rf)
    # ヘッダー行を飛ばす
    next(reader)
    with open(write_path, mode="w", encoding="utf-8", newline='') as wf:
      writer = csv.writer(wf)
      writer.writerow(["word", "meanings", "score"])
      for line in reader:
        if(str == line[0]):
          # print(str)
          writer.writerow([line[0], line[1], Scores[score]])
        else:
          writer.writerow([line[0], line[1], line[2]])


def editDictionary(read_info, eiken_paths, adding_path):
  for path in eiken_paths:
    print("** "+ path + " **********")
    list = path.split("/")
    fname = list[len(list)-1]
    fname = re.sub(".*-", "", fname)
    score = re.sub(".txt", "", fname)
    with open(path, mode="r", encoding="utf-8") as f:
      str = f.read()
      list = str.split(",")
      for l in list:
        editScore(read_info["dir"], adding_path, read_info["fname"], l, score)
        write_path = adding_path + read_info["fname"] + l[0].upper() + ".csv" 
        move_path = read_info["dir"] + read_info["fname"] + l[0].upper() + ".csv"
        shutil.move(write_path, move_path)



def main():
  csv_path = "../DictionaryMaker/dictionary/EngTrans_"
#   csv_paths=[]
  eiken_paths=[]
  e_path = "../dictionary/eiken/"
  eikens = ["tango-5", "tango-4", "tango-3", "tango-pre2", "tango-2", "tango-pre1", "tango-1"]
  for e in eikens:
    eiken_paths.append(e_path+e+".txt")
#   Alphabet = string.ascii_uppercase
#   Alphabet = list(Alphabet)
#   for a in Alphabet:
#     csv_paths.append(path+a+".csv")
  # editDictionary("../dictionary/English_Trans/EngTrans_", eiken_paths)

if __name__ == "__main__":
  main()