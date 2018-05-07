#encoding=utf-8

import re
import random
import copy
import openpyxl
import pandas as pd

type_list = list()
locate_list = list()
year_list = list()
food_list = list()
des_list = list()
variety_list = list()
page_list = list()
multi_list = list()
other_list = list()

training_data = open("redwine_training_data_musk.iob", "r").readlines()
training_data_expend = open("redwine_dataset_musk_expend.iob", "w")
#other_type_data = open("./dataset/ijia_dataset_othertype.iob","r").readlines()

#entity_type =openpyxl.load_workbook(file)
#sheets = entity_type.sheetnames
#sheet1 = sheets[1]
#ws = entity_type.get_sheet_by_name(sheet1)

data = pd.read_csv("entity_type_redwine.csv")
#print(data.iloc[1:20,4])
l = len(data)

def add_sentance(list, label, tar_label=""):
    print("========== 正在處理 " + label + " ===========")

    for i in range(1,9):
        if tar_label == "":
            if data.iloc[0,i] == label:
                ws_colum = i
                #print(i)
                break
        else:
            if data.iloc[0, i] == tar_label:
                ws_colum = i
                break
    else:
        print("no label match")

    for row in range(1,l):
        if row%500 == 0:
            print("已處理 " +str(row)+" 筆資料")

        word = data.iloc[row,ws_colum]
        if type(word) != type(0.0):
            sentance_index = random.randint(0,len(list)-1)
            word_index = list[sentance_index][1].index(label)
            #expend_sentance = copy.deepcopy( list[sentance_index] )
            expend_sentance = copy.deepcopy(list[sentance_index])
            expend_sentance[0][word_index] = word

            if tar_label != "":
                expend_sentance[1][word_index] = tar_label

            a = " ".join( expend_sentance[0] )
            b = " ".join( expend_sentance[1] )
            s = a + "\t" + b + " " + expend_sentance[2]

            training_data_expend.write( s )
        else:
            break

def add_multi_entity_sentance(list, label):
    print("========== 正在處理 " + label + " ===========")
    for i in range(1,21):
        if data.iloc[0,i] == label:
            ws_colum = i
            #print(i)
            break
    else:
        print("no label match")

    for row in range(1,l):
        if row%500 == 0:
            print("已處理 " +str(row)+" 筆資料")

        word = data.iloc[row,ws_colum]
        if type(word) != type(0.0):
            sentance_index = random.randint(0,len(list)-1)
            word_index = list[sentance_index][1].index(label)
            #expend_sentance = copy.deepcopy( list[sentance_index] )
            expend_sentance = copy.deepcopy(list[sentance_index])
            expend_sentance[0][word_index] = word

            a = " ".join( expend_sentance[0] )
            b = " ".join( expend_sentance[1] )
            s = a + "\t" + b + " " + expend_sentance[2]

            training_data_expend.write( s )
        else:
            break

def add_single_entity_sentence(entity,intent):
    for i in range(1,21):
        if data.iloc[0,i] == entity:
            ws_colum = i
            #print(i)
            break
    else:
        print("no label match")

    for row in range(1,l):
        if row%500 == 0:
            print("已處理 " +str(row)+" 筆資料")

        word = data.iloc[row,ws_colum]
        if type(word) != type(0.0):


            a = "BOS " + word + " EOS"
            b = "O " + entity
            s = a + "\t" + b + " " + intent + "\n"

            training_data_expend.write( s )
        else:
            break


for t in training_data:
    #train_data = re.sub("\n", "", line).sub("\t", " ", line).split(" ")
    train_data = [t.split( "\t" )[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]]

    if "B-年份" in train_data[1]:
        year_list.append(train_data)
    if "B-产区" in train_data[1]:
        locate_list.append(train_data)
    if "B-葡萄品种" in train_data[1]:
        variety_list.append(train_data)
    if "B-酒种类" in train_data[1]:
        type_list.append(train_data)
    if "B-食物" in train_data[1]:
        food_list.append(train_data)
    if "B-页面" in train_data[1]:
        page_list.append(train_data)
    if "B-酒属性" in train_data[1]:
        des_list.append( train_data )
    if "B-年份" in train_data[1] and "B-产区" in train_data[1] and \
            "B-葡萄品种" in train_data[1] and "B-酒种类" in train_data[1]:
        multi_list.append(train_data)

    if train_data[2] == "语音辅助\n" or train_data[2] == "页面引导\n" or train_data[2] == "库存\n":
        other_list.append(t)


add_sentance(des_list,"B-酒属性")
add_sentance(year_list,"B-年份")
add_sentance(locate_list,"B-产区")
add_sentance(variety_list,"B-葡萄品种")
add_sentance(type_list,"B-酒种类")
add_sentance(food_list,"B-食物")
add_sentance(page_list,"B-页面")
add_sentance(locate_list,"B-产区","B-国家")



year = [tag for tag in data.iloc[1:,4] if type(tag) != type(0.0)]
variety = [tag for tag in data.iloc[1:,5] if type(tag) != type(0.0)]
_type = [tag for tag in data.iloc[1:,1] if type(tag) != type(0.0)]

for i in range(1,l):
    locate = data.iloc[i,2]
    if type(locate) != type(0.0):
        sentence_index = random.randint(0,len(multi_list)-1)
        sentence = copy.deepcopy(multi_list[sentence_index])
        year_index = multi_list[sentence_index][1].index("B-年份")
        variety_index = multi_list[sentence_index][1].index("B-葡萄品种")
        type_index = multi_list[sentence_index][1].index("B-酒种类")

        rand_year = year[random.randint(0,len(year)-1)]
        rand_variety = variety[random.randint( 0, len( variety ) - 1 )]
        rand_type = _type[random.randint( 0, len( _type ) - 1 )]

        sentence[0][year_index] = rand_year
        sentence[0][variety_index] = rand_variety
        sentence[0][type_index] = rand_type

        a = " ".join( sentence[0] )
        b = " ".join( sentence[1] )
        s = a + "\t" + b + " " + sentence[2]
        print(s)
        training_data_expend.write( s )

#add_sentance(build_list,"B-餐廳需求::地標")
#add_sentance(mrt_list,"B-餐廳需求::捷運站")
#add_sentance(curse_list,"B-對罵")
#add_sentance(hello_list,"B-打招呼")
#add_single_entity_sentence("B-餐廳需求::店名","找餐廳")
#add_single_entity_sentence("B-餐廳需求::類型","找餐廳")
#add_single_entity_sentence("B-餐廳需求::餐點","找餐廳")
#add_single_entity_sentence("B-餐廳需求::地點","找餐廳")

for i in other_list:
    #a = " ".join( i[0] )
    #b = " ".join( i[1] )
    #s = a + "\t" + b + " " + i[2]

    training_data_expend.write( i )