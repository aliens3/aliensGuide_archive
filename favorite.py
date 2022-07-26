import os 
import csv
import re

#medium_list = ["movie","book","paper","blog","youtube"]
medium_list = ["movie"]

for medium in medium_list :
    csv_name = medium + ".csv"
    csv_path = os.path.join("./_data/",csv_name)
    a=os.path.join(".",medium)

    # md_listはindex.md以外のフォルダ内のmdファイル
    md_list=os.listdir(a)
    md_list.remove("index.md")
    title=""
    title_to_mdURL_name={}
    # 日本語タイトルからURLへ変換
    for md in md_list:
        md_path = os.path.join(a,md)
        md_name=md.split(".")[0]
        md_url=os.path.join("/",medium,md_name)
        with open(md_path) as f:
            Lines = f.readlines()
            for line in Lines:
                if line.startswith("title:"):
                    title=line.replace(" ","").replace(":","").replace("\n","").replace("title","")
                    title_to_mdURL_name[title]=md_url
                    break
    print(title_to_mdURL_name)
    table_text=""
    with open(csv_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile,delimiter=',')
        sorted_spamreader=sorted(spamreader, key=lambda student: student[0]) 
        for i,row in enumerate(sorted_spamreader):
            print(row)
            if not row[0] in title_to_mdURL_name:
                table_text += "|" + row[0] + "|" + row[1] + "\n"
            else:
                table_text += "|" + f"<a href=\"{title_to_mdURL_name[row[0]]}\"> " + row[0] + "</a>" + "|" + row[1] + "\n"
            if i == 0:
                table_text += "| --------- | \n"
    print(table_text)
    
    index_path = os.path.join("./",medium,"index.md")
    with open(index_path) as idx:
        txt=idx.read()
        #newtxt=txt.replace("####InsertTable####",table_text)
        newtxt= re.sub('<!-- cut# -->[\S\s]*?<!-- endcut# -->', f'<!-- cut# -->\n\n\n{table_text}\n<!-- endcut# -->', txt)
        print(newtxt)
    with open(index_path, "w") as f:
        f.write(newtxt)