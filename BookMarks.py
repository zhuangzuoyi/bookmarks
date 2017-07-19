import re
import json
import chardet
import codecs
import time


#str = str.replace("\n","")

#root is dict
def find_list(root):
    mark_list=[]
    for item_root in root:
        if type(root[item_root]) is dict:
            #print("\tDict:%s,%s" %(item_root, type(root[item_root])))
            list_temp=find_list(root[item_root])
            for it in list_temp:
                mark_list.append(it)
        elif type(root[item_root])  is list:
            #print("\t\tList:%s" %item_root)
            mark_list.append(root[item_root])
        else:
            if len(root) >= 5:
                pass
            print("\tTEXT:%s,%s" %(type(root[item_root]),root[item_root]))

    return mark_list
    
    
#child is a  list,dict in list
def find_url(child):
    all_data=""
    format_dat=""
    di_ty=dict()
    empty=dict()
    print("Start find url")
    for ma_0 in child:
        print("%s" %type(ma_0))
        if ma_0.get("url") is None:
            print("no url,%s" %(type(ma_0)))
            
            for i in ma_0:
                print("\t%s:%s" %(i,type(ma_0[i])))
                if type(ma_0[i]) is list:
                    print("\t%s"  %("<"*10))
                    str_temp,empty = find_url(ma_0[i])
                    #format_dat = format_dat + str_temp
                    print("\t%s" %(">"*10))
            if type(ma_0) is dict:
                if "type" in ma_0 and "name" in ma_0:
                    print("\t\t\tFourder:%s" %(ma_0["name"]))
                    di_ty.update({ma_0["name"]:str_temp})
                else:
                    format_dat = format_dat + str_temp
            else:
                format_dat = format_dat + str_temp
            print("\t\t\tEMPTY:%d" %(len(empty)))
            if len(empty) != 0:
                di_ty.update(empty)
        else:
            last = ma_0["name"] + ":" + ma_0["url"] + "\n"
           # print("\t%s" %last)
            format_dat = format_dat + last
    return format_dat,di_ty

#child is a  list,dict in list
def find_url_str(child):
    format_dat=""
    print("Start find url")
    for ma_0 in child:
        print("%s" %type(ma_0))
        if ma_0.get("url") is None:
            print("no url,%s" %(type(ma_0)))
            
            for i in ma_0:
                print("\t%s:%s" %(i,type(ma_0[i])))
                if type(ma_0[i]) is list:
                    print("\t%s"  %("<"*10))
                    str_temp = find_url_str(ma_0[i])
                    format_dat = format_dat + str_temp
                    print("\t%s" %(">"*10))     
        else:
            last = ma_0["name"] + ":" + ma_0["url"] + "\n"
           # print("\t%s" %last)
            format_dat = format_dat + last
    return format_dat
    
def read_bookmarks():
    bookmark=r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\bookmarks"
    line=""
    fd=open(bookmark,'rb')
    line=fd.read()
    print("The head is:%x,%x,%x" %(line[0],line[1],line[2]))
    #utf-8 BOM 
    if line[0] ==0xef and line[1]==0xbb and line[2] ==0xbf:
        print("BOM")
        str = line[3:].decode("utf-8")   
    else:
        str=line.decode('utf-8')
    fd.close()
    return str

    
def make_dict():
    bo_st=read_bookmarks()    
    print("--Start--")
    book=json.loads(bo_st)
    print("Root's type:%s" %type(book))
    print("start analysis")
    list_l = find_list(book)
    print(len(list_l))
    last_str=""
    main_dict=dict()
    for ma in list_l:
        print(len(ma))
        str_0,dic = find_url(ma)
        last_str=  last_str+ str_0
        main_dict.update(dic)
    main_dict.update({"ROOT":last_str})
    print("Main dict:%d" %(len(main_dict)))
    print("*"*20)
    for ke in main_dict:
        print(ke)
        print(main_dict[ke])
    print("5"*10)
    return main_dict
    #print(last_str)
    
    
def make_bookmark_str():
    bo_st=read_bookmarks()    
    print("--Start--")
    book=json.loads(bo_st)
    print("Root's type:%s" %type(book))
    print("start analysis")
    list_l = find_list(book)
    print(len(list_l))
    last_str=""
    for ma in list_l:
        print(len(ma))
        str_0 = find_url_str(ma)
        last_str=  last_str+ str_0
    print("5"*10)
    return last_str
    #print(last_str)

    
if __name__=="__main__":
    l_str=make_bookmark_str()
    ti=time.strftime("%Y%m%d", time.localtime())
    new_fd = open(ti,'w')
    new_fd.write(l_str)
    new_fd.close()
    make_dict()