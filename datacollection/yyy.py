# -*- coding: utf-8 -*-

import c_k_data_tushare as c
import f_analysis_get_ma20 as f
import g_analysis_turningpoint as g
import h_turningpoint as h
import i_query as i

if __name__ == '__main__':

    print(time.time())
    c.move_history()
    print(time.time())
    c.bulk_insert_tushare_data()
    print(time.time())
    print("all done...")


    print(time.time())
    f.move_history()
    print(time.time())
    f.bulk_get_ma20_and_insert()
    print(time.time())
    print("all done...")


    print(time.time())
    g.move_history()
    print(time.time())
    g.bulk_get_ma20_and_insert()
    print(time.time())
    print("all done...")


    i.query()
    print("all done...")

#end
