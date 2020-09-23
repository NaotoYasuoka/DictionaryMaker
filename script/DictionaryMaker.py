import os, csv
import sys
import string
import re
import alkana
import urllib.request
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from pykakasi import kakasi
from kanjize import int2kanji, kanji2int

from make_baseform import english_to_kana as etok

import sys
sys.path.append('../')
import __init__ as init


# PartOfSpeech={"名":True, "不":False, "副":False, "形":False, "雑誌名":True, "商標":True, "他動":False, "間投":False, "人名":False, "組織":True, "著作":True, "映画":True, "地名":True, "連結":False, "自動":False, "バンド名":True, "省略形":False}
PartOfSpeech={"名":True, "不":True, "副":True, "形":True, "雑誌名":True, "商標":True, "他動":True, "間投":True, "人名":False, "組織":True, "著作":True, "映画":True, "地名":True, "連結":True, "自動":True, "バンド名":True, "省略形":True, "動":True, "新聞名":True}
alphabet={"A":"エー", "B":"ビー", "C":"シー", "D":"ディ", "E":"イー", "F":"エフ", "G":"ジー", "H":"エイチ", "I":"アイ", "J":"ジェー", "K":"ケイ", "L":"エル", "M":"エム", "N":"エヌ", "O":"オウ", "P":"ピー", "Q":"キュウ", "R":"アール", "S":"エス", "T":"ティー", "U":"ユー", "V":"ブイ","W":"ダブル", "X":"エックス", "Y":"ワイ", "Z":"ゼット"}
Symbols={"+":"プラス", "-":"マイナス", "℃":"ド", "α":"アルファ", "β":"ベータ", "×":"バツ", "χ":"カイ", "？":"クエスチョンマーク", "γ":"ガンマ", "Δ":"デルタ", "ζ":"ゼータ", "η":"イータ", "θ":"シータ", "ι":"イオタ", "κ":"カッパ", "λ":"ラムダ", "μ":"ミュー", "ν":"ミュー", "ξ":"クシー", "ο":"オミクロン", "π":"パイ", "ρ":"ロー", "σ":"シグマ", "τ":"タウ", "υ":"ウプシロン", "φ":"ファイ", "ψ":"プシー", "Ω":"オメガ"}
Number={"0":"れい", ".":"てん"}
symbol={"《":"《.*》", "〔":"〔.*〕", "〈":"〈.*〉", "（":"（.*）", "［":"［.*］"}



# https://qiita.com/tame3_4dream/items/1dc46838747dc692d4da
def english_to_katakana(word):
  url = 'https://www.sljfaq.org/cgi/e2k_ja.cgi'
  url_q = url + '?word=' + word
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}

  request = urllib.request.Request(url_q, headers=headers)
  html = urllib.request.urlopen(request)
  soup = BeautifulSoup(html, 'html.parser')
  katakana_string = soup.find_all(class_='katakana-string')[0].string.replace('\n', '')

  return katakana_string


def makeMean(str):
  splitStr = str.lstrip(" ")
  mean = splitStr.split('◆')[0]
  mean = mean.split('【')[0]
  mean = mean.split('■')[0]
  mean = mean.split('＝<')[0]
  mean = mean.split('〈英〉')[0]
  mean = mean.split('<→')[0]
  mean = re.sub("＝", "", mean)
  mean = re.sub("…", "", mean)
  return mean

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



k = kakasi()  # Generate kakasi instance
k.setMode('J', 'H') #漢字からひらがなに変換
k.setMode('K', 'H')
conv = k.getConverter()

def English_to_Kana(str, fname):
  read = str.strip()
  english = re.compile('[a-zA-Z]+')
  words = english.findall(read)
  if((len(words) >= 1) & (fname == "EngDict_")):
    for w in words:
      if(len(w) == 1):
        furigana = alphabet.get(w.upper())
        read = read.replace(w, furigana)
      else:
        count = 0
        for i in range(len(w)):
          if (w[i] >= "A") & (w[i] <= "Z"):
            count+=1 
          if(count >= len(w)/2):
            for i in range(len(w)):
              furigana = alphabet.get(w[i].upper())
              if((w[i] in read) | (furigana != None)):
                read = read.replace(w[i], furigana)
          # else:
            # e2k = etok.EnglishToKana()
            # furigana = e2k.convert(w)
            # if(furigana != "ERROR 辞書にありません"):
            # read = read.replace(w, furigana)
  # 英語訳しりとりモードの辞書作成
  else:
    if(len(words) >= 1):
      for w in words:
        if(len(w) == 1):
          furigana = alphabet.get(w.upper())
          read = read.replace(w, furigana)
        else:
          count = 0
          for i in range(len(w)):
            count+=1 if (w[i] >= "A") & (w[i] <= "Z") else 0
          if(count >= len(w)/2):
            for i in range(len(w)):
              furigana = alphabet.get(w[i].upper())
              if((w[i] in read) | (furigana != None)):
                read = read.replace(w[i], furigana)
          else:
            read = ""      

  numbers = re.findall(r'[0-9]+\.?[0-9]*', read)
  if(len(numbers) >= 1):
    for n in numbers:
      if("." in n):
        for i in range(len(n)):
          if((n[i] == ".") | (n[i] == "0")):
            furigana = Number.get(n[i])
          else:
            furigana = int2kanji(int(n[i]))
          read = read.replace(n[i], furigana)
      else:
        furigana = int2kanji(int(n))
        read = read.replace(n, furigana)
  for s in Symbols.keys():
    if(s in Symbols):
      read = read.replace(s, Symbols[s])
  if(read != ""):
    read = conv.do(read)
    # if((read[0] >= "あ") & (read[0] <= "ん") | (read[-1] >= "あ") & (read[-1] <= "ん")):
    return str+","+conv.do(read)
    # else:
      # return None
  else:
    return None



def editMeans(str, fname):
  means_list = []
  str = makeMean(str)
  if(fname == "EngTrans_"):
    str = removeSymbol(str)
  str = str.replace("（", "(")
  str = str.replace("）", ")")
  list = str.split("、")
  if(len(list) != 0):
    for s in list:
      if(s != ""):
        if((s[0] == "～") | (s[0] == "「") | (s[0] == "『") | (s[0] == "＿") | (s[0] == "○")):
          s = ""
      if(s != ""):
        mean = English_to_Kana(s, fname)
        if(mean != None):
          means_list.append(mean)  
  if(means_list != []):
    return means_list
  else:
    return None



def edit_Dictionary(read_paths, save_info):
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
        word = re.sub("\{.*\}", "", w)
        pos = re.findall('\{.*\}', w)
        word = word.rstrip()
        pos = classification_PoS(pos)
        if(None != pos):
          mean = editMeans(m, save_info["fname"])
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
                  # saveFile(save_info["dir"]+save_info["fname"]+leadAlphabet+".csv", "word", "meanings", "score")
                  # print(old_word, pos, means_txt)
                  print(leadAlphabet+"を書き込み中")
                # print(pos, old_word, means_txt)
                init.Add_WriteFile(save_info["dir"]+save_info["fname"]+leadAlphabet+".csv", old_word, means_txt, int(0))
                # saveFile(save_info["dir"]+save_info["fname"]+leadAlphabet+".csv", old_word, means_txt, int(0))
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