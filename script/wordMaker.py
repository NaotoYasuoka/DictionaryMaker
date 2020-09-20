from bs4 import BeautifulSoup as BS
import requests
import os, csv
import re
#-*- coding: utf-8 -*-

def get_tables(content, is_talkative=True):
    """table要素を取得する"""
    bs = BS(content, "lxml")
    tables = bs.find_all("table")
    n_tables = len(tables)
    if n_tables == 0:
        emsg = "table not found."
        raise Exception(emsg)
    if is_talkative:
        print("%d table tags found.." % n_tables)
    return tables

def parse_table(table):
    """table要素のデータを読み込んで二次元配列を返す"""

    ##### thead 要素をパースする #####

    # thead 要素を取得 (存在する場合)
    thead = table.find("thead")

    # thead が存在する場合
    if thead:
        tr = thead.find("tr")
        ths = tr.find_all("th")
        columns = ths
        #columns = [th.text for th in ths]    # pandas.DataFrame を意識
    
    # thead が存在しない場合
    else:
        columns = []

    ##### tbody 要素をパースする #####

    # tbody 要素を取得
    tbody = table.find("tbody")

    # tr 要素を取得
    trs = tbody.find_all("tr")

    # 出力したい行データ
    rows = [columns][0]

    # td (th) 要素の値を読み込む
    # tbody -- tr 直下に th が存在するパターンがあるので
    # find_all(["td", "th"]) とするのがコツ
    for tr in trs:
        row = [td.text for td in tr.find_all(["td", "th"])]
        rows.append(row)

    return rows


def table2csv(path, rows, lineterminator="\n",
    is_talkative=True):
    """二次元データをCSVファイルに書き込む"""

    # 安全な方に転ばせておく
    if os.path.exists(path):
        emsg = "%s already exists." % path
        raise ValueError(emsg)

    # データを書き込む
    with open(path, "w") as f:
        writer = csv.writer(f, lineterminator=lineterminator)
        writer.writerows(rows)
        if is_talkative:
            print("%s successfully saved." % path)


def main():
    # HTML データを取得する
    # url = "https://eikentry.com/tango/tango-5"
    urls = ["https://eikentry.com/tango/tango-5", "https://eikentry.com/tango/tango-4", "https://eikentry.com/tango/tango-3", "https://eikentry.com/tango/tango-pre2", "https://eikentry.com/tango/tango-2", "https://eikentry.com/tango/tango-pre1", "https://eikentry.com/tango/tango-1"]
    i=0
    for url in urls:
        text=""
        list = url.split("/")
        fname = list[len(list)-1]
        res = requests.get(url)
        content = res.text
        rows = []
        # table 要素を取得する
        # HTML 中のすべての table 要素が表として使われているとも
        # 限らないし、またそれが望んでいるものであるとも限らないので
        # このあたりのプロセスは関数としてまとめていない
        # ( = テーブルの選択自体はユーザーが行う)
        tables = get_tables(content)
        for table in tables:
            #table = tables[0]
            rows.append(parse_table(table)) #= parse_table(table)
            #print(rows)
        for row in rows:
            for cell in row:
                i+=1
                #print(cell[0])
                text += str(cell[0]) + ","
        text = text.rstrip(",")
        writepath = '../dictionary/eiken/'+str(fname)+".txt"
        with open(writepath, mode="w", encoding="utf-8") as f:
            f.write(text)
    print("wordNum", i)




if __name__ == "__main__":
    main()
#text.split("(", ")")
# savetext=""
#splitWord = text.split("[()（）]",txt)
# splitWord = text.replace(" ", "")
# for word in splitWord:
#     words = word.split("（")
# for word in words:
#     words = word.split("）")
# for word in words:
#     words = word.split(")")
# print(splitWord)
# i=0
# for word in splitWord:
#     if(i % 2 == 0):
#         savetext += word
#     i=i+1

# print(savetext)

##print(s.rstrip('abc'))
# CSV ファイルとして出力する
# 出力先が Windows なら以下のようにする
#table2csv("./table.csv", rows, "\r\n")