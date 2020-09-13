import os, csv
import sys

def divideText(path):

  # readlineで1行だけ読み込み
  #with open(path, "r", encoding="Shift_JIS") as f:
  with open(path, "r", encoding="utf-8") as f:
    line = f.readline()
    while line:
      Str = line.rstrip()   # 改行の削除
      str = Str.lstrip("■") # "■"の削除
      if(((str[0]>="A") | (str[0]>="a")) & ((str[0]<="Z") | (str[0]<="z"))):
        #print(str)
        splitStr = str.split(":")
        words = splitStr[0]
        means = splitStr[1]

        #word = words.replace("\{", "")
        word = words.rstrip('  {')
         #word = re.sub(r'\{[^)]*\}', '', words)
        print(word)

        # with open('sample.csv', 'a') as f_a:
          # print(word+","+means, file=f_a)
        
      #else:
        #print("Error: configuration failed", file=sys.stderr)
      line = f.readline()

def main():
  original_data_path = "./dictionary/EIJIROU.txt"
  divideText(original_data_path)

if __name__ == "__main__":
    main()