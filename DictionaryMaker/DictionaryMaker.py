import os, csv
import sys
import string

def makeWord(str):
  words = str.split(" ")
  word = None
  if(len(words) == 1):
    word = words[0]
  return word

def makeMean(str):
  splitStr = str.lstrip(" ")
  mean_1 = splitStr.split('◆')[0]
  mean_2 = mean_1.split('【')[0]
  mean_3 = mean_2.split('■')[0]
  mean_4 = mean_3.split('＝<')[0]
  mean_5 = mean_4.split('〈英〉')[0]
  mean_6 = mean_5.split('<→')[0]
  return mean_6
  
def wordNumber(str):
  strlist=[]
  word_means = str.split(":")
  word_pos = word_means[0]
  means = word_means[1]
  word=makeWord(word_pos)
  if(word != None):
    mean=makeMean(means)
    strlist.append(word)
    strlist.append(mean)
  else:
    strlist = None
  return strlist


# def divideText(path, write_path):
#   word = ""
#   means = ""
#   # readlineで1行だけ読み込み
#   with open(path, "r", encoding="utf-8") as f:
#     # with open(write_path, mode="a", encoding="utf-8",newline='') as w:
#     with open(write_path, mode="a", encoding="utf-8") as w:
#       with open("./dictionary/EIJIRO_N-Z.txt", mode="a", encoding="utf-8") as ws:
#   #with open(path, "r", encoding="utf-8") as f:
#         line = f.readline()
#         i = 0
#         while line:
#           str = line   # 改行の削除
#         # str = Str.lstrip("■") # "■"の削除
#         # str1 = str.rstrip(" ")
#           if(((str[1]>="A")  & (str[1]<="Z")) | ((str[1]>="a") & (str[1]<="z"))):
#             if(((str[1]>="A")  & (str[1]<="M")) | ((str[1]>="a") & (str[1]<="m"))):
#               w.write(str)
#             if(((str[1]>="N")  & (str[1]<="Z")) | ((str[1]>="n") & (str[1]<="z"))):
#               ws.write(str)
#             i+=1
#           # list=wordNumber(str)
#           # if(list != None):
#           #   if(word == list[0]):
#           #     if(list[1]!=""):
#           #       means += ","+list[1]
#           #   else:
#           #     if((word != "") & (means != "")):
#           #       writer = csv.writer(w)
#           #       writer.writerow([word,means])
#           #       word = ""
#           #       means = ""
#           #       # w.write(word+","+means+"\n")
#           #     word = list[0]
#           #     means = list[1]
#           # else:
#           #   print("2単語以上で、対象外です...")
#           # w.writer(str)
#             print(str)
#           else:
#             print("A-Z(a-z)以外の語から始まる単語です...")
#             #w.write(str+"\n")
          
#           line = f.readline()
#         print(i)
      # if((word != "") & (means != "")):
      #   writer = csv.writer(w)
      #   writer.writerow([word,means])

def divideText(str):
  obj={}
  splitStr = str.split(":")
  str1 = splitStr[0].rstrip("{")
  #obj["word"] = str1
  #obj["means"] = splitStr[1]
  return obj

def read_write_File(read_paths, write_path, writeType):
  for r_path in read_paths:
    # with open(r_path, "r", encoding="utf-8") as r_f:
    with open(r_path, mode="r", encoding="cp932") as r_f:
      line = r_f.readline()
      while line:
        #wordInfo = divideText(line)
        saveFile(write_path, line, writeType)
        line = r_f.readline()

def saveFile(write_path, wordInfo, writeType):
  #if((wordInfo["word"] != "") & (wordInfo["means"] != "")):
    if("csv" == writeType):
      with open(write_path, "a", encoding="utf-8",newline='') as w_f:
        writer = csv.writer(w_f)
        writer.writerow([wordInfo["word"],wordInfo["means"]])
    elif("txt" == writeType):
      if(((wordInfo[1]>="A")  & (wordInfo[1]<="M")) | ((wordInfo[1]>="a") & (wordInfo[1]<="m"))):
        with open(write_path, "a", encoding="utf-8",newline='') as w_f:
          w_f.write(wordInfo)
    elif("test" == writeType):
      print(wordInfo["word"]+":"+wordInfo["means"])
    else:
      print("The only read types are 'csv' and 'txt'.",file=sys.stderr)


def divideFile():
  # 辞書の細分化
  with open("../../../dictionary/EIJIRO-1448.TXT", mode="r", encoding="cp932") as r_f:
    with open("./dictionary/EIJIRO_A-M.txt", mode="a", encoding="utf-8") as w_f_a:
      with open("./dictionary/EIJIRO_N-Z.txt", mode="a", encoding="utf-8") as w_f_n:
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
  divideFile()
  read_paths = ["../../../dictionary/EIJIRO-1448.TXT"]
  # read_path = "../../../dictionary/EIJIRO_.txt"
  #read_paths = ["./dictionary/EIJIRO_A-M.txt", "./dictionary/EIJIRO_N-Z.txt"]
  #read_path = "./dictionary/test_EIJIRO.txt"
  #read_path = "../../../dictionary/EIJIRO_.txt"
  # write_path = "./dictionary/EIJIRO_treatment.csv"
  write_path = "./dictionary/EIJIRO_A-M.txt"
  # read_write_File(read_paths, write_path, "txt")

if __name__ == "__main__":
    main()