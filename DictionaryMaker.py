import os, csv
import sys

def makeWord(str):
  words = str.split(" ")
  word = None
  if(len(words) == 1):
    word = words[0]
  # for w in words:
  #   i=0
  #   if((i==1) & (w == "")):
  #     #print(w)
  #     word = words[0]
  #   i=i+1
  return word

def makeMean(str):
  splitStr = str.lstrip(" ")
  # pos = str.find('◆')
  # mean = str[:pos]
  mean_1 = splitStr.split('◆')[0]
  mean_2 = mean_1.split('【')[0]
  mean_3 = mean_2.split('■')[0]
  mean_4 = mean_3.split('＝<')[0]
  mean_5 = mean_4.split('〈英〉')[0]
  mean_6 = mean_5.split('<→')[0]
  # mean_3 = mean_2.rstrip("■")
  # pos = mean_1.find('【')
  # mean_2 = mean_1[:pos]
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


def divideText(path, write_path):
  word = ""
  means = ""
  # readlineで1行だけ読み込み
  with open(path, "r", encoding="utf-8") as f:
  #with open(path, "r", encoding="cp932") as f:
    with open(write_path, mode="a", encoding="utf-8",newline='') as w:
  #with open(path, "r", encoding="utf-8") as f:
      line = f.readline()
      while line:
        Str = line.rstrip()   # 改行の削除
        str = Str.lstrip("■") # "■"の削除
        if(((str[0]>="A")  & (str[0]<="Z")) | ((str[0]>="a") & (str[0]<="z"))):
          list=wordNumber(str)
          if(list != None):
            if(word == list[0]):
              if(list[1]!=""):
                means += ","+list[1]
            else:
              if((word != "") & (means != "")):
                writer = csv.writer(w)
                writer.writerow([word,means])
                word = ""
                means = ""
                # w.write(word+","+means+"\n")
              word = list[0]
              means = list[1]
          else:
            print("2単語以上で、対象外です...")
        else:
          print("A-Z(a-z)以外の語から始まる単語です...")
            #w.write(str+"\n")
        line = f.readline()
      if((word != "") & (means != "")):
        writer = csv.writer(w)
        writer.writerow([word,means])

def main():
  #original_data_path = "../../dictionary/EIJIRO-1448.TXT"
  #original_data_path = "./dictionary/EIJIROU.txt"
  read_path = "../../dictionary/EIJIRO_.txt"
  write_path = "../../dictionary/EIJIRO_treatment.csv"
  divideText(read_path, write_path)

if __name__ == "__main__":
    main()