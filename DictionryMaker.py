import os, csv

def divideText(path):

  # readlineで1行だけ読み込み
  with open(path, "r", encoding="Shift_JIS") as f:
    line = f.readline()
    # print(line)
    while line:
      str = line.lstrip("■")
      if((str[0] <= "A" | str[0] <= "L") & (str[0] <= "a" | str[0] <= "l")):
        print(line)
    #   # ...
    #   line = f.readline()
    # str = line.lstrip("■")
    # if((str[0] <= "A" | str[0] <= "L") & (str[0] <= "a" | str[0] <= "l")):
    #   print(line)
  # f.close()

def main():
  original_data_path = "./dictionary/EIJIROU.txt"
  divideText(original_data_path)

if __name__ == "__main__":
    main()