# -*- coding: utf-8 -*-


ths_stock_list_file = "E:\\Table.txt"

def read_table_txt():
    stock_list = []
    stock_market_list = []
    list_of_stock_dict = []

    with open(ths_stock_list_file, "r", encoding = "gbk") as f:
        lines = f.readlines()
        for row in lines[1:]:
            stock_dict = {}
            r = row.replace("\t", "").replace("\n", "")
            if len(r) > 8:
                market = r[0:2]
                code = r[2:8]
                name = r[8:]
                #print(market, code, name)
                stock_dict["code"] = code
                stock_dict["name"] = name
                stock_dict["market"] = market

                stock_list.append(code)
                stock_market_list.append(r[0:8])
                list_of_stock_dict.append(stock_dict)

    #print(len(lines))
    #print(len(stock_list))
    #print(stock_list)
    return stock_list, stock_market_list, list_of_stock_dict


def update_mongo_basic_data():
    sl, cl, d = read_table_txt()
    print(sl)
    print(cl)
    print(d)
    print(len(sl))
    print(len(cl))
    print(len(d))



    print("done")


if __name__ == '__main__':

#end
