import os
import re
import csv

dict_path = "./dictionary/"
# それぞれのモードのファイル
AddingSco_path =dict_path + "Adding_score/"
EngTrans_path = dict_path + "English_Trans/"
EngDict_path = dict_path + "English_Dict/"
JapTrans_path = dict_path + "Japanese_Trans/"
# ファイル名の形式とパス
EngTrans_file_path = EngTrans_path + "EngTrans_A.csv"
EngDict_file_path = EngDict_path + "EngDict_A.csv"
# EngDict_file_path = JapTrans_path + "EngDict_A.csv"
JapTrans_file_path = JapTrans_path + "JapTrans_あ.csv"
# 辞書のパス
dictionary_paths = ["./dictionary/EIJIRO_A-M.txt", "./dictionary/EIJIRO_N-Z.txt"]
# eikenのデータのパス
eiken_paths = ["./dictionary/eiken/tango-5.txt", "./dictionary/eiken/tango-4.txt", "./dictionary/eiken/tango-3.txt", "./dictionary/eiken/tango-pre2.txt", "./dictionary/eiken/tango-2.txt", "./dictionary/eiken/tango-pre1.txt", "./dictionary/eiken/tango-1.txt"]

# csv_path = "./dictionary/English_Trans/EngTrans_"
# csv_path = "./dictionary/English_Dict/EngDict_"

# 使用する品詞情報
EngTrans_PoS = {"名":True, "不":False, "副":False, "形":False, "雑誌名":True, "商標":True, "他動":False, "間投":False, "人名":False, "組織":True, "著作":True, "映画":True, "地名":True, "連結":False, "自動":False, "バンド名":True, "省略形":False}
EngDict_PoS = {"名":True, "不":True, "副":True, "形":True, "雑誌名":True, "商標":True, "他動":True, "間投":True, "人名":False, "組織":True, "著作":True, "映画":True, "地名":True, "連結":True, "自動":True, "バンド名":True, "省略形":True, "動":True, "新聞名":True}

# 使用する情報
EngDict_Info = { "read_path": dictionary_paths,
                 "write_path" : EngDict_file_path,
                 "work_dir"  : AddingSco_path,
                 "eiken_path": eiken_paths,
                 "pos"       : EngDict_PoS
               }

EngTrans_Info = { "read_path": dictionary_paths,
                  "write_path" : EngTrans_file_path,
                  "work_dir"  : AddingSco_path,
                  "eiken_path": eiken_paths,
                  "pos"       : EngTrans_PoS
               }


# ファイル情報の取得
def fileInfo(str):
  dir = ""
  dic = {}
  path = str.split("/")
  for i in range(len(path)-1):
    dir += path[i] + "/"
  file = path[len(path)-1]
  file = re.sub("_.*", "", file)
  file += "_"
  dic["dir"] = dir
  dic["fname"] = file
  return dic


# ファイルへの書き込み
def Add_WriteFile(write_path, str1, str2, score):
  if(os.path.isfile(write_path) == True):
    with open(write_path, "a", encoding="utf-8",newline='') as w_f:
      writer = csv.writer(w_f)
      writer.writerow([str1, str2, score])
  else:
    with open(write_path, "a", encoding="utf-8",newline='') as w_f:
      writer = csv.writer(w_f)
      pathInfo = fileInfo(write_path)
      if(pathInfo["fname"] == "JapTrans_"):
        writer.writerow(["meanings", "word", "score"])
      else:
        writer.writerow(["word", "meanings", "score"])
      writer.writerow([str1, str2, score])