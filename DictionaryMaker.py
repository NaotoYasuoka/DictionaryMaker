import os, csv
import sys

def makeWord(str):
  words = str.split(" ")
  word = None
  if(len(words) == 1):
    word = words[0]
  for w in words:
    i=0
    if((i==1) & (w == "")):
      word = words[0]
    i=i+1
  return word

def makeMean(str):

  return None
  
def wordNumber(str):
  strlist=[]
  word_means = str.split(":")
  word_pos = word_means[0]
  means = word_means[0]

  # if((word=makeWord(word_pos)) != None):
  #   makeMean(means)

  return makeWord(word_pos)

def divideText(path, write_path):
  # readlineで1行だけ読み込み
  # with open(path, "r", encoding="Shift_JIS") as f:
  with open(path, "r", encoding="cp932") as f:
    with open(write_path, mode="a", encoding="utf-8") as w:
  #with open(path, "r", encoding="utf-8") as f:
      line = f.readline()
      while line:
        Str = line.rstrip()   # 改行の削除
        str = Str.lstrip("■") # "■"の削除
        if(((str[0]>="A") | (str[0]>="a")) & ((str[0]<="Z") | (str[0]<="z"))):
          # if(wordNumber(str) != None):
          w.write(str+"\n")
        line = f.readline()

def main():
  original_data_path = "../../dictionary/EIJIRO-1448.TXT"
  write_path = "../../dictionary/text.txt"
  divideText(original_data_path, write_path)

if __name__ == "__main__":
    main()