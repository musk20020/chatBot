#encoding=utf-8

import re
import random
import copy

train_data_list = list()
shop_locate_list = list()
locate_food_list = list()
locate_type_list = list()
shop_list = list()
locate_list = list()
type_list = list()
food_list = list()
training_data = open("./dataset/ijia_dataset.iob", "r").readlines()
training_data_expend = open("ijia_dataset_expend.iob", "w")

road_dict = './jieba-zh_TW/road_dic_musk.txt'
type_dict = './jieba-zh_TW/type_dic.txt'
food_dict = './jieba-zh_TW/food_dic.txt'
restaurant_dict = './jieba-zh_TW/Restaurant_dic.txt'
mrt_station_dict = './jieba-zh_TW/mrt_station_dic_musk.txt'
dict_road = open(road_dict, "r").readlines()
dict_type = open(type_dict, "r").readlines()
dict_food = open(food_dict, "r").readlines()
dict_shop = open(restaurant_dict, "r").readlines()
dict_mrt = open(mrt_station_dict, "r").readlines()



for t in training_data:
    #train_data = re.sub("\n", "", line).sub("\t", " ", line).split(" ")
    train_data = [t.split( "\t" )[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]]

    if train_data[2] == "找餐廳\n":
        if "B-餐廳需求::店名" in train_data[1] and "B-地點" in train_data[1]:
            shop_locate_list.append(train_data)
        elif "B-地點" in train_data[1] and "B-餐廳需求::餐點" in train_data[1]:
            locate_food_list.append(train_data)
        elif "B-地點" in train_data[1] and "B-餐廳需求::類型" in train_data[1]:
            locate_type_list.append(train_data)
        elif "B-餐廳需求::店名" in train_data[1]:
            shop_list.append(train_data)
        elif "B-地點" in train_data[1]:
            locate_list.append(train_data)
        elif "B-餐廳需求::餐點" in train_data[1]:
            food_list.append(train_data)
        elif "B-餐廳需求::類型" in train_data[1]:
            type_list.append(train_data)

for shop in dict_shop:
    shop = re.sub(" 5\n", "", shop)
    shop = re.sub(" ", "", shop)
    random_index = random.randint(0, len(dict_road)-1)
    road = re.sub("\r\n", "", dict_road[random_index])

    sentance_index = random.randint(0,len(shop_locate_list)-1)
    shop_index = shop_locate_list[sentance_index][1].index("B-餐廳需求::店名")
    locate_index = shop_locate_list[sentance_index][1].index("B-地點")

    expend_sentance = copy.deepcopy(shop_locate_list[sentance_index])
    expend_sentance[0][shop_index] = shop
    expend_sentance[0][locate_index] = road

    a = " ".join(expend_sentance[0])
    b = " ".join(expend_sentance[1])
    s = a+"\t"+b+" "+expend_sentance[2]

    training_data_expend.write(s)

for mrt in dict_mrt:
    mrt = re.sub( "\r\n", "", mrt )
    random_index = random.randint( 0, len( dict_food ) - 1 )
    food = re.sub( "\n", "", dict_food[random_index] )

    sentance_index = random.randint( 0, len( locate_food_list ) - 1 )
    food_index = locate_food_list[sentance_index][1].index( "B-餐廳需求::餐點" )
    locate_index = locate_food_list[sentance_index][1].index( "B-地點" )

    expend_sentance = copy.deepcopy( locate_food_list[sentance_index] )
    expend_sentance[0][food_index] = food
    expend_sentance[0][locate_index] = mrt

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )

for type in dict_type:
    type = re.sub( "\n", "", type )
    random_index = random.randint( 0, len( dict_road ) - 1 )
    road = re.sub( "\r\n", "", dict_road[random_index] )

    sentance_index = random.randint( 0, len( locate_type_list ) - 1 )
    type_index = locate_type_list[sentance_index][1].index( "B-餐廳需求::類型" )
    locate_index = locate_type_list[sentance_index][1].index( "B-地點" )

    expend_sentance = copy.deepcopy( locate_type_list[sentance_index] )
    expend_sentance[0][type_index] = type
    expend_sentance[0][locate_index] = road

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )

for shop in dict_shop:
    shop = re.sub( " 5\n", "", shop )
    shop = re.sub( " ", "", shop )

    sentance_index = random.randint( 0, len( shop_list ) - 1 )
    shop_index = shop_list[sentance_index][1].index( "B-餐廳需求::店名" )

    expend_sentance = copy.deepcopy( shop_list[sentance_index] )
    expend_sentance[0][shop_index] = shop

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )

for food in dict_food:
    food = re.sub( "\n", "", food )

    sentance_index = random.randint( 0, len( food_list ) - 1 )
    food_index = food_list[sentance_index][1].index( "B-餐廳需求::餐點" )

    expend_sentance = copy.deepcopy( food_list[sentance_index] )
    expend_sentance[0][food_index] = food

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )

for type in dict_type:
    type = re.sub( "\n", "", type )

    sentance_index = random.randint( 0, len( type_list ) - 1 )
    type_index = type_list[sentance_index][1].index( "B-餐廳需求::類型" )

    expend_sentance = copy.deepcopy( type_list[sentance_index] )
    expend_sentance[0][type_index] = type

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )

for locate in dict_road:
    road = re.sub( "\r\n", "", locate )

    sentance_index = random.randint( 0, len( locate_list ) - 1 )
    locate_index = locate_list[sentance_index][1].index( "B-地點" )

    expend_sentance = copy.deepcopy( locate_list[sentance_index] )
    expend_sentance[0][locate_index] = road

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )

for locate in dict_mrt:
    mrt = re.sub( "\r\n", "", locate )

    sentance_index = random.randint( 0, len( locate_list ) - 1 )
    locate_index = locate_list[sentance_index][1].index( "B-地點" )

    expend_sentance = copy.deepcopy( locate_list[sentance_index] )
    expend_sentance[0][locate_index] = mrt

    a = " ".join( expend_sentance[0] )
    b = " ".join( expend_sentance[1] )
    s = a + "\t" + b + " " + expend_sentance[2]

    training_data_expend.write( s )