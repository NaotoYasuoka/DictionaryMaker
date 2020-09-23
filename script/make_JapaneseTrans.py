import re, os, csv, glob
import sys
sys.path.append('../')
import __init__ as init

def division_Means(str):
  means_list=[]
  list = str.split("_")
  for l in list:
    mean = l.split(",")
    list = []
    for m in mean:
      m = re.sub("\(.*\)", "", m)
      list.append(m)
    means_list.append(list)
  return means_list

def make_JapaneseTrans(read_info, write_info):
  files = glob.glob(read_info["dir"]+"*.csv")
  for file in files:
    file = file.replace("\\", "/")
    with open(file, mode="r", encoding="utf-8") as rf:
      reader = csv.reader(rf)
      # ヘッダー行を飛ばす
      next(reader)
      for line in reader:
        word = line[0]
        means = line[1]
        means_list = division_Means(means)
        for ml in means_list:
          mean = ml[0]
          kana = ml[1]

          init.Add_WriteFile(write_info["dir"]+write_info["fname"]+kana[0]+".csv", mean+","+kana, word, line[2])