# -*- coding:utf-8 -*-
import time
import re
import codecs
import BookMarks
import os

footer_file_name = "footer.txt"
context=""
body_file_name = "20170420"
target_file_name=""


index_header="""<!DOCTYPE html> 
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>20170424</title>
        <meta name="viewport" content="width=device-width">

        <!-- syntax highlighting CSS -->
        <link rel="stylesheet" href="src/css/syntax.css">

        <!-- Custom CSS -->
        <link rel="stylesheet" href="src/css/main.css">
    </head>
    <body>
<div class="site">
  <div class="header">
    <div class="rotateID">
        <h1 class="title">Chrome BookMarks</h1>
    </div>
  </div>


<div id="home">

<hr> """

index_footer="""</div>
          <div class="footer">
            <div class="contact">
              <p>
                Power  :<br />
              </p>
            </div>
            <div class="contact">
              <p>
                <a> Python</a><br />
              </p>
            </div>
          </div>
        </div>
    </body>
</html>"""
#make header
#make target file name
def get_header():
    #create target file name
    header_file_name = "header.txt"
    title=time.strftime("%Y%m%d", time.localtime())
    target_file_name ="src/" + title+".html"

    #create header
    header_fd = open(header_file_name,"r")
    header_template= header_fd.read()
    #target_re = re.compile("{%title%}")
    header = re.sub("{%title%}",title,header_template)
    header_fd.close()
    return header,target_file_name
    
def get_fooder():
    #create footer
    footer_fd = open(footer_file_name,'r')
    footer = footer_fd.read()
    footer_fd.close()
    return footer

    
def mar():
    #create target file name
    title=time.strftime("%Y%m%d", time.localtime())
    target_file_name = title+".html"

    #create header
    header_fd = open(header_file_name,"r")
    header_template= header_fd.read()
    #target_re = re.compile("{%title%}")
    header = re.sub("{%title%}",title,header_template)
    context = context + header
    header_fd.close()

    #create body
    head_of_ur='\n<ul class="arc-list">'
    end_of_ur='</ul> \n'
    con_of_ur=""
    #body_fd = open(body_file_name,"r")
    body_fd = codecs.open(body_file_name, "r", "utf-8")
    while True:
        line = body_fd.readline()
        if len(line)>0:
            res=re.search(":http",line)
            ind = line.find(":http")
            print(ind)
            print(line[0:ind]+"  :  "+line[ind+1:-1])
            if ind != -1:
                con_of_ur = con_of_ur + "<li ><a href=\"" + line[ind+1:-2] +  "\">" + line[0:ind] + '</a></li>' + '\n'
        else:
            break
    context = context + head_of_ur + con_of_ur +  end_of_ur  
    body_fd.close()       


    #create footer
    footer_fd = open(footer_file_name,'r')
    footer = footer_fd.read()
    context = context + footer
    footer_fd.close()
    #create target file
    #target_fd = open(target_file_name,'w')
    target_fd = codecs.open(target_file_name, "w", "utf-8")
    target_fd.write(context)
    target_fd.close()

def make_body_form_dict():
    dic = BookMarks.make_dict()
    head_of_ur='\n<ul class="arc-list">'
    end_of_ur='</ul> \n'
    con_of_ur=""
    for item in dic:
        print(item)
        con_of_ur = con_of_ur + "<h3>"+item+"</h3>"+'\n'
        url_list = dic[item].split('\n')
        for url in url_list:
            res=re.search(":http",url)
            ind = url.find(":http")
            print(url)
            print(ind)
            #print(url[0:ind]+"  :  "+url[ind+1:-1])
            if ind != -1:
                con_of_ur = con_of_ur + "<li ><a href=\"" + url[ind+1:] +  "\">" + url[0:ind] + '</a></li>' + '\n'
                print("add")
    return head_of_ur+con_of_ur+end_of_ur

def update_index():
    names = os.listdir('src')
    title='\n<ul class="arc-list">'

    for na in names:
        if na.endswith(".html"):
            nam=na.split('.')
            title = title + "<li><a href=\"" + "src/"+na +"\">" + nam[0] + '</a></li>' + '\n'
    title = title+'</ul> \n'
    index = index_header + title + index_footer
    
    index_fd = codecs.open("index.html", "w", "utf-8")
    index_fd.write(index)
    index_fd.close()
    
    
if __name__=="__main__":
    print("Hello")
    print(BookMarks.make_bookmark_str())
    head,target_file_name=get_header()

    print(target_file_name)

    l_s=head+ make_body_form_dict() +get_fooder()
    
    target_fd = codecs.open(target_file_name, "w", "utf-8")
    target_fd.write(l_s)
    target_fd.close()
    update_index()