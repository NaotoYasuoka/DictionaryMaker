import os, csv
import string
import shutil
import re

def editScore(str, fname, csv_path):
  path = csv_path + str[0].upper() + ".csv"
  write_path = "../dictionary/Adding_score/EngTrans_"+str[0].upper()+".csv"
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
          print(fname)
          writer.writerow([line[0], line[1], fname])
        else:
          writer.writerow([line[0], line[1], line[2]])


def editDictionary(csv_path, eiken_paths):
  d = csv_path.split("/")
  n = len(d)
  dir = ""
  for i in range(n-1):
    dir += d[i] + "/"
  print(dir)
  for path in eiken_paths:
    print("** "+ path + " **********")
    list = path.split("/")
    fname = list[len(list)-1]
    fname = re.sub(".*-", "", fname)
    fname = re.sub(".txt", "", fname)
    with open(path, mode="r", encoding="utf-8") as f:
      str = f.read()
      list = str.split(",")
      for l in list:
        editScore(l, fname, csv_path)
        write_path = '../dictionary/Adding_score/EngTrans_'+l[0].upper()+".csv"
        move_path = dir + 'EngTrans_'+l[0].upper()+".csv"
        
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
  editDictionary("../dictionary/English_Trans/EngTrans_", eiken_paths)

if __name__ == "__main__":
  main()