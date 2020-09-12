import os, csv

def divideText(path):

  # readlineで1行だけ読み込み
  with open(path, "r", encoding="utf_8") as f:
    line = f.readline()
    while line:
      try:
        line = line.decode("utf-8")
      except UnicodeDecodeError:
        # utf-8でないバイト列が含まれる行はスキップする
        line = f.readline()
        continue
        # ...
      # 何か行いたい処理
      str = line.lstrip("■")
      if((str[0] <= "A" | str[0] <= "L") & (str[0] <= "a" | str[0] <= "l")):
        print(line)
      # ...
    #   line = f.readline()
    # str = line.lstrip("■")
    # if((str[0] <= "A" | str[0] <= "L") & (str[0] <= "a" | str[0] <= "l")):
    #   print(line)
  # f.close()

def main():
  original_data_path = "../../Dictionary/EIJIRO-1448.TXT"
  divideText(original_data_path)

if __name__ == "__main__":
    main()