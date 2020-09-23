import os, csv, glob
import urllib.request
from bs4 import BeautifulSoup
import __init__ as init
from script import DictionaryMaker as dm
from script import uniteDictionary as ud
from script import make_JapaneseTrans as mJ

from kanjize import int2kanji, kanji2int


Scores={"5":1, "4":2, "3":3, "pre2":4, "2":5, "pre1":6, "1":7, "-":0}

def assign_Scores(read_info, write_dir):
  files = glob.glob(read_info["dir"]+"*.csv")
  for file in files:
    file = file.replace("\\", "/")
    file_info = init.fileInfo(file)
    with open(file,  mode="r", encoding="utf-8") as rf:
      reader = csv.reader(rf)
      next(reader)
      for line in reader:
        score = Scores.get(line[2])
        fname = line[0]
        init.Add_WriteFile(write_dir+file_info["fname"]+fname[0].upper()+".csv", line[0], line[1], score)



def main():

  # file_info = init.EngTrans_Info
  file_info = init.EngDict_Info

  write_info = init.fileInfo(file_info["write_path"])

  dm.edit_Dictionary(file_info["read_path"], write_info)
  ud.editDictionary(write_info, file_info["eiken_path"], file_info["work_dir"])

  # assign_Scores(write_info, file_info["work_dir"])


  # read_info = init.fileInfo(init.EngTrans_file_path)
  # write_info = init.fileInfo(init.JapTrans_file_path)
  # mJ.make_JapaneseTrans(write_info, init.fileInfo(init.JapTrans_file_path))


if __name__ == "__main__":
  main()