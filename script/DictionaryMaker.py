import os, csv
import sys
import string
import re
import alkana
from janome.tokenizer import Tokenizer
from pykakasi import kakasi



PartOfSpeech={"名":True, "不":False, "副":False, "形":False, "雑誌名":True, "商標":True, "他動":False, "間投":False, "人名":False, "組織":True, "著作":True, "映画":True, "地名":True, "連結":False, "自動":False, "バンド名":True, "省略形":False}
# symbol=["《", "〔", "〈", "（", "［"]
symbol={"《":"《.*》", "〔":"〔.*〕", "〈":"〈.*〉", "（":"（.*）", "［":"［.*］"}

def makeMean(str):
  splitStr = str.lstrip(" ")
  mean_1 = splitStr.split('◆')[0]
  mean_2 = mean_1.split('【')[0]
  mean_3 = mean_2.split('■')[0]
  mean_4 = mean_3.split('＝<')[0]
  mean_5 = mean_4.split('〈英〉')[0]
  mean_6 = mean_5.split('<→')[0]
  return mean_6

def divideText(str):
  obj={}
  splitStr = str.split(":")
  str1 = splitStr[0].rstrip("{")
  #obj["word"] = str1
  #obj["means"] = splitStr[1]
  return obj


def removeSymbol(str):
  symbols = symbol.keys()
  for s in symbols:
    if s in str:
      str = re.sub(symbol[s], "", str)
  return str



def classification_PoS(list):
  pos_list = []
  plist = []
  if(len(list) != 0):
    str = list[0].lstrip("{")
    str = str.rstrip("}")
    list = str.split("・")
    for p in list:
      value = re.sub("^[0-9]", "", p)
      value = re.sub("[0-9]*$","", value)
      value = value.strip("-")
      pos_list.append(value)
    for p in pos_list:
      j = PartOfSpeech.get(p)
      if(j == True):
        plist.append(p)
    if(len(plist) == 0):
      return None
    else:
      return plist
  else:
    return None


def editMeans(str):
  means_list = []
  str = makeMean(str)
  str = removeSymbol(str)
  list = str.split("、")
  k = kakasi()  # Generate kakasi instance
  k.setMode('J', 'H') #漢字からひらがなに変換
  k.setMode('K', 'H')
  conv = k.getConverter()
  if(len(list) != 0):
    for s in list:
      if(s != ""):
        means_list.append(s+","+conv.do(s))
  if(means_list != []):
    return means_list
  else:
    return None


def edit_Dictionary(read_paths):
  write_path="../dictionary/English_Trans/EngTrans_"
  leadAlphabet = ""
  old_word = ""
  means_list = []
  for r_path in read_paths:
    with open(r_path, mode="r", encoding="utf-8") as r_f:
      line = r_f.readline()
      while line:
        str = line.rstrip()
        str = str.lstrip("■")
        word_means = str.split(":")
        w = word_means[0]
        m = word_means[1]
        # w = re.sub('.*\{', "", w)
        # pos = re.sub('\}', "", pos)
        word = re.sub("\{.*\}", "", w)
        pos = re.findall('\{.*\}', w)
        word = word.rstrip()
        pos = classification_PoS(pos)
        if(None != pos):
          mean = editMeans(m)
          if(None != mean):
            if(old_word == word):
              for m in mean:
                if(m in means_list):
                  mean.pop(mean.index(m))
              means_list += mean
            else:
              means_txt = ""
              if(old_word != ""):
                for m in means_list:
                  means_txt += m + "_"
                means_txt = means_txt.rstrip("_")
                if(leadAlphabet != old_word[0].upper()):
                  leadAlphabet = old_word[0].upper()
                  saveFile(write_path+leadAlphabet+".csv", "word", "meanings", "score")
                  # print(old_word, pos, means_txt)
                  print(leadAlphabet+"を書き込み中")
                # print(pos, old_word, means_txt)
                saveFile(write_path+leadAlphabet+".csv", old_word, means_txt, "-")
              old_word = word
              # means_list = []
              means_list = mean
        line = r_f.readline()



def saveFile(write_path, word, means, score):
  with open(write_path, "a", encoding="utf-8",newline='') as w_f:
    writer = csv.writer(w_f)
    writer.writerow([word,means, score])



def divideFile():
  # 辞書の細分化(A-M, N-Z)
  with open("../../../dictionary/EIJIRO-1448.TXT", mode="r", encoding="cp932") as r_f:
    with open("../dictionary/EIJIRO_A-M.txt", mode="a", encoding="utf-8") as w_f_a:
      with open("../dictionary/EIJIRO_N-Z.txt", mode="a", encoding="utf-8") as w_f_n:
        line = r_f.readline()
        i = 0
        while line:
          str = line
          if(((str[1]>="A")  & (str[1]<="M")) | ((str[1]>="a") & (str[1]<="m"))):
            w_f_a.write(str)
          if(((str[1]>="N")  & (str[1]<="Z")) | ((str[1]>="n") & (str[1]<="z"))):
            w_f_n.write(str)
          i+=1
          line = r_f.readline()
        print("word num:", i)


def main():
  # divideFile()
  # read_paths = ["../../../dictionary/EIJIRO-1448.TXT"]
  # read_path = "../../../dictionary/EIJIRO_.txt"
  read_paths = ["../dictionary/EIJIRO_A-M.txt", "../dictionary/EIJIRO_N-Z.txt"]
  #read_path = "./dictionary/test_EIJIRO.txt"
  #read_path = "../../../dictionary/EIJIRO_.txt"
  # write_path = "./dictionary/EIJIRO_treatment.csv"
  write_path = "./dictionary/EIJIRO_A-M.txt"
  # read_write_File(read_paths, write_path, "txt")
  edit_Dictionary(read_paths)
  # str = "aiiiii"
  # str = str.split(",")
  # print(str)

if __name__ == "__main__":
    main()