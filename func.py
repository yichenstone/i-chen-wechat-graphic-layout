import tkinter
from tkinter import filedialog
import re
from bs4 import BeautifulSoup
import os
import json
import requests
import random
from datetime import date, timedelta
import base64

registered = "0" #判断用户是否已注册
item_style = "1" #样式记录
changed = "0" #控制转换后左边html切换，0为left.html本身改变，1为left.html被Sample.html替代
title_name = "用户转换后保存内容的文件名"
img_divider = "https://re-yichen.oss-cn-beijing.aliyuncs.com/img/divider.png" #默认分割线
icon_author = " "

def GetValue(from_html):
    # 注册工具
    if from_html == "hello":
        global registered
        registered ="1"
        return "registered$已注册"

    # 上传文件
    elif from_html =="up_file":
        root = tkinter.Tk()
        root.withdraw() #不显示主窗体
        root.wm_attributes('-topmost', 1) #置顶显示对话框
        file_path = filedialog.askopenfilename(title='选择你需要转换的文件',filetypes=[('Html Md', '*.html *.md'), ('All Files', '*')]) # [('Html Doc Docx', '*.html *.doc *.docx'), ('All Files', '*')]
        if file_path =="":
            Fpath = "up_link$文件路径"
        else:
            Fpath = "up_link$" + file_path
        return Fpath

    # 读取高级设置json文件并传值到前端
    elif from_html == "adSetReceive":
        with open("./配置文件.json", "r+",encoding="utf-8") as file:
            f1 = file.read()
        return "adSetReceive$" + f1

    # 保存高级设置json文件
    elif from_html[:9] == "adSetSave":
        json_data = from_html[10:]
        with open("./配置文件.json", "w+",encoding="utf-8") as file:
            file.write(json_data)
            file.close()
        return "adSetSave$保存成功"

    # 接收item_style传值，切换left和right样式
    elif from_html[:10] == "item_style":
        global item_style
        item_style = from_html.split("$")[1]
        try:
            ItemChange(item_style) #定义了一个函数
            return "item_style$选择样式" + item_style
        except:
            return "item_style$样式选择错误"

    # 立即排版
    elif from_html[:5] =="style":
        style = from_html.split("$")[0]
        up_file_link = from_html.split("$")[1]
        if up_file_link != "文件路径":
            MainConversion(style[6:],up_file_link)
            if item_style =='003':
                if registered =="0":
                    return "changeBlindBoxError$点亮您的SVIP，体验盲盒乐趣"
                if changed =="1":
                    return "changeBlindBox$排版完成"
                else:
                    return "changeBlindBoxError$未找到该主题icon，请重新设置"
            else:
                return "change$排版完成"
        else:
            return "rechange$请选择需要转换的文件"


    # 保存每个样式的css
    elif from_html[:4] == "save":
        css_link = from_html.split("$")[1]
        css_text = from_html.split("$")[2]
        # print(css_link)
        # print(css_text)
        with open("./items_css/right.html", "r+",encoding="utf-8") as file:
            f1 = file.read()
            # 此处正则，使用sub直接替换，会将textarea也替换掉，采用以下方案处理
            css_text_1 = '<textarea rows="35" cols="20" class="out_text" name="textarea" id="item_text" charset="utf-8">' + css_text + '</textarea>'
            f1 = re.sub('<textarea([\s\S]*?)</textarea>',css_text_1,f1)
        with open("./items_css/item_"+item_style+".html", "w+",encoding="utf-8") as file:
            file.write(f1)
            file.close()
        with open("./items_css/right.html", "w+",encoding="utf-8") as file:
            file.write(f1)
            file.close()
        with open("./sample/sample"+item_style+".html", "r+",encoding="utf-8") as file:
            f2 = file.read()
            # 此处正则，使用sub直接替换，会将textarea也替换掉，采用以下方案处理
            css_text_2 = '<style type="text/css">' + css_text + '</style>'
            f2 = re.sub('<style([\s\S]*?)</style>',css_text_2,f2)
        with open("./sample/sample"+item_style+".html", "w+",encoding="utf-8") as file:
            file.write(f2)
            file.close()
        with open("./left.html", "r+",encoding="utf-8") as file:
            f3 = file.read()
            # 此处正则，使用sub直接替换，会将textarea也替换掉，采用以下方案处理
            css_text_2 = '<style type="text/css">' + css_text + '</style>'
            f3 = re.sub('<style([\s\S]*?)</style>',css_text_2,f3)
        with open("./left.html", "w+", encoding="utf-8") as file:
            file.write(f3)
            file.close()
        return "save$css保存完成"

    #重置CSS
    elif from_html == "reset_css":
        ResetCss()
        return "reset_css$样式" + item_style + "css重置完成"

    # 退出修改为默认首页
    elif from_html == "exit":
        # 修改左右两侧的页面为默认页面
        with open("./items_css/item_default.html", "r+", encoding="utf-8") as file:
            f1 = file.read()
        with open("./items_css/right.html", "w+", encoding="utf-8") as file:
            file.write(f1)
            file.close()
        with open("./sample/sample_default.html", "r+", encoding="utf-8") as file:
            f2 = file.read()
        with open("./left.html", "w+", encoding="utf-8") as file:
            file.write(f2)
            file.close()
        return "exit$退出"
        # sys.exit()

def ItemChange(item_style):
    # 修改左右两侧的页面为样式一对应页面.将对应页面copy到left.html和right.html
    with open("./items_css/item_" + item_style + ".html", "r+", encoding="utf-8") as file:
        f1 = file.read()
    with open("./items_css/right.html", "w+", encoding="utf-8") as file:
        file.write(f1)
        file.close()
    if changed == "0":
        with open("./sample/sample" + item_style + ".html", "r+", encoding="utf-8") as file:
            f2 = file.read()
        with open("./left.html", "w+", encoding="utf-8") as file:
            file.write(f2)
            file.close()
    else:
        # 获取css样式
        with open("./items_css/item_" + item_style + ".html", "r+", encoding="utf-8") as file:
            f1 = file.read()
            f1 = BeautifulSoup(f1, 'html.parser')
            f1 = f1.find_all('textarea')[0].text
        with open("./left.html", "r+", encoding="utf-8") as file:
            f2 = file.read()
            css_text = '<style type="text/css">' + f1 + '</style>'
            f2 = re.sub('<style([\s\S]*?)</style>', css_text, f2)

        # 替换关键词样式
        f2 = ReplaceKeywordStyle(f2) #函数

        with open("./left.html", "w+", encoding="utf-8") as file:
            file.write(f2)
            file.close()
        with open("./历史排版/"+title_name+".html", "w+", encoding="utf-8") as file:
            file.write(f2)
            file.close()

def ResetCss():
    # 将备份css保存到对应item和right.html中
    with open("./items_css/backup_css/item_" + item_style + ".html", "r+", encoding="utf-8") as file:
        f1 = file.read()
    with open("./items_css/item_" + item_style + ".html", "w+", encoding="utf-8") as file:
        file.write(f1)
        file.close()
    with open("./items_css/right.html", "w+", encoding="utf-8") as file:
        file.write(f1)
        file.close()
    with open("./sample/sample" + item_style + ".html", "r+", encoding="utf-8") as file:
        f2 = file.read()
        # 此处正则，使用sub直接替换，会将textarea也替换掉，采用以下方案处理
        css_text = re.findall('<textarea rows="35" cols="20" class="out_text" name="textarea" id="item_text" charset="utf-8">([\s\S]*?)</textarea>',f1)[0]
        css_text_2 = '<style type="text/css">' + css_text + '</style>'
        f2 = re.sub('<style([\s\S]*?)</style>', css_text_2, f2)
    with open("./sample/sample" + item_style + ".html", "w+", encoding="utf-8") as file:
        file.write(f2)
        file.close()
    with open("./left.html", "w+", encoding="utf-8") as file:
        file.write(f2)
        file.close()

def MainConversion(item_style,up_file_link):
    # print(item_style)
    # print(up_file_link)
    global changed  # 转换完成后changed取值变为1
    if up_file_link[-2:] == "md":
        changed = MdConver(up_file_link)
    else:
        changed = HtmlConver(up_file_link)

#以下是md文件转换功能的主要函数
def MdConver(up_file_link):
    # 获取css样式
    if item_style == "003":  # css盲盒
        html_head_style = BlindBox()
        if html_head_style == "0":
            return "0"  # 0表示icon没有找到
    else:
        with open("./items_css/item_" + item_style + ".html", "r+", encoding="utf-8") as file:
            f1 = file.read()
            html_head_style = re.findall(
                '<textarea rows="35" cols="20" class="out_text" name="textarea" id="item_text" charset="utf-8">([\s\S]*?)</textarea>',
                f1)[0]

    # 获取用户自定义关键词
    with open("./配置文件.json", "r+", encoding='utf-8') as file:
        json_data = file.read()
        json_data = json.loads(json_data)
    keyword_1 = json_data['keyWords'][0]['name']
    keyword_2 = json_data['keyWords'][1]['name']
    keyword_3 = json_data['keyWords'][2]['name']

    # 获取md内容
    try:
        with open(up_file_link, "r+", encoding="utf-8") as file:
            md = file.readlines()
            md[0]=md[0][1:] # 清除文本格式说明
    except:
        try:
            with open(up_file_link, "r+", encoding="gbk") as file:
                md = file.readlines()
        except:
            with open(up_file_link, "r+", encoding="utf-16") as file:
                md = file.readlines()

    title = up_file_link.split("/")[-1][:-3]  # 拿到标题

    # 转换后html的head
    html_head = '<!DOCTYPE html><html><head><meta charset="utf-8"><style type="text/css">' + html_head_style + '</style><script src="js/left.js" type="text/javascript" charset="utf-8"></script></head><body><span class="body" style="display:block;"><h1></h1>'
    if item_style == "003":  # 这里有个困难，公众号后台以读取到文字开始拉取，如果文字前有svg图片，不会拉取到
        html_head = '<!DOCTYPE html><html><head><meta charset="utf-8"><style type="text/css">' + html_head_style + '</style><script src="js/left.js" type="text/javascript" charset="utf-8"></script></head><body><span class="body" style="display:block;"><h1></h1><p style="color: #55B494;">图文中部分样式来自www.iconfont.cn，限个人使用</br>icon作者：' + icon_author + '</br>这段话复制到公众号后台可删除</p>'
    else:
        pass

    new_html = []
    new_html.append(html_head)
    mdCount = 0 # 初始参数
    mark_ul = 0
    mark_ol = 0
    mark_bl = 0

    for item in md:
        mdCount = mdCount + 1

        # 清洗无效数据
        if item[:] == ">\n":  # 无效引用
            continue
        elif item[:] == "\n" and md[mdCount - 2] != "\n":  # 消除标题后的无效空行
            continue
        else:
            pass

        # 文字加粗、斜体、下划线
        for i in range(50):  # 处理加粗
            try:
                onespan = re.findall('\*\*(.*?)\*\*', item)[0]
                if onespan=='':
                    break
                else:
                    onetext = DealWord(['bold'], onespan)  # 加粗
                    item = item.replace('**' + onespan + '**', onetext)
            except:
                break
        for i in range(50):  # 处理斜体
            try:
                onespan = re.findall('\*(.*?)\*', item)[0]
                if onespan=='':
                    break
                else:
                    onetext = DealWord(['italic'], onespan)  # 斜体
                    item = item.replace('*' + onespan + '*', onetext)
            except:
                break
        for i in range(50):  # 处理下划线
            try:
                onespan = re.findall('<u>(.*?)</u>', item)[0]
                if onespan=='':
                    break
                else:
                    onetext = DealWord(['underline'], onespan)  # 下划线
                    item = item.replace('<u>' + onespan + '</u>', onetext)
            except:
                break

        # 引用
        if item[:2] == "> ":
            if mark_ul == 1:
                new_html.append("</ul>")
                mark_ul = 0
            elif mark_ol == 1:
                new_html.append("</ol>")
                mark_ol = 0
            else:
                pass
            one_text = item[2:-1]
            bl = '<blockquote data-tool="一陈图文排版">'
            if new_html[len(new_html) - 1][:3] != "<bl" and new_html[len(new_html) - 1][:20] != '<p class="citation">':
                one_text = bl + '<p class="citation">' + one_text + "</p>"
                mark_bl = 1
            else:
                one_text = '<p class="citation">' + one_text + "</p>"
                mark_bl = 1
            new_html.append(one_text)
            continue
        elif mark_bl != 0:
            new_html[len(new_html) - 1] = new_html[len(new_html) - 1] + "</blockquote>"
            mark_bl = 0
        else:
            pass

        # 列表
        if item[:2] == "- ":  # 无序列表
            one_text = item[2:-1]
            ul = '<ul>'
            if new_html[len(new_html) - 1][:3] != "<ul" and new_html[len(new_html) - 1][:3] != "<li":
                one_text = ul + "<li>" + one_text + "</li>"
                mark_ul = 1
            else:
                one_text = "<li>" + one_text + "</li>"
                mark_ul = 1
            new_html.append(one_text)
            continue
        elif item[1:3] == ". " or item[2:4] == ". ":  # 有序列表
            one_text = item[:-1]
            ol = '<ol>'
            if new_html[len(new_html) - 1][:3] != "<ol" and new_html[len(new_html) - 1][:3] != "<li":
                if one_text[1:3] == ". ":
                    one_text = ol + "<li>" + one_text[3:] + "</li>"
                else:
                    one_text = ol + "<li>" + one_text[4:] + "</li>"
                mark_ol = 1
            else:
                if one_text[1:3] == ". ":
                    one_text = "<li>" + one_text[3:] + "</li>"
                else:
                    one_text = "<li>" + one_text[4:] + "</li>"
                mark_ol = 1
            new_html.append(one_text)
            continue
        elif mark_ul == 1:
            new_html[len(new_html) - 1] = new_html[len(new_html) - 1] + "</ul>"
            mark_ul = 0
        elif mark_ol == 1:
            new_html[len(new_html) - 1] = new_html[len(new_html) - 1] + "</ol>"
            mark_ol = 0
        else:
            pass

        # 标题
        if item[:2] == "# ":  # 一级标题
            one_text = item[2:-1]
            try:
                one_text = re.sub('<span class=".*?">', "", one_text)
                one_text = re.sub('</span>', "", one_text)
                one_text = re.sub('<font color.*?>', "", one_text)
                one_text = re.sub('</font>', "", one_text)
                one_text_1 = one_text.split(" ", 1)
                one_text = '<h1 data-tool="一陈图文排版" ><img class="h1_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h1_svg_box"><svg class="h1_svg"></svg></span><span class="h1_num">' + \
                       one_text_1[0] + '</span><span class="text">' + one_text_1[1] + '</span></h1>'
            except:
                one_text = '<h1 data-tool="一陈图文排版" ><img class="h1_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h1_svg_box"><svg class="h1_svg"></svg></span><span  class="text_noNum">' + one_text + '</span></h1>'
            new_html.append(one_text)
            continue
        elif item[:3] == "## ":  # 二级标题
            one_text = item[3:-1]
            try:
                one_text = re.sub('<span class=".*?">', "", one_text)
                one_text = re.sub('</span>', "", one_text)
                one_text = re.sub('<font color.*?>', "", one_text)
                one_text = re.sub('</font>', "", one_text)
                one_text_1 = one_text.split(" ", 1)
                one_text = '<h2 data-tool="一陈图文排版" ><img class="h2_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h2_svg_box"><svg class="h2_svg"></svg></span><span class="h2_num">' + \
                        one_text_1[0] + '</span><span  class="text">' + one_text_1[1] + '</span></h2>'
            except:
                one_text = '<h2 data-tool="一陈图文排版" ><img class="h2_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h2_svg_box"><svg class="h2_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h2>'
            new_html.append(one_text)
            continue
        elif item[:4] == "### ":  # 三级标题
            one_text = item[4:-1]
            try:
                one_text = re.sub('<span class=".*?">', "", one_text)
                one_text = re.sub('</span>', "", one_text)
                one_text = re.sub('<font color.*?>', "", one_text)
                one_text = re.sub('</font>', "", one_text)
                one_text_1 = one_text.split(" ", 1)
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="h3_num">' + \
                       one_text_1[0] + '</span><span  class="text">' + one_text_1[1] + '</span></h3>'
            except:
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h3>'
            new_html.append(one_text)
            continue
        elif item[:5] == "#### ":  # 四级标题
            one_text = item[5:-1]
            try:
                one_text = re.sub('<span class=".*?">', "", one_text)
                one_text = re.sub('</span>', "", one_text)
                one_text = re.sub('<font color.*?>', "", one_text)
                one_text = re.sub('</font>', "", one_text)
                one_text_1 = one_text.split(" ", 1)
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="h3_num">' + \
                        one_text_1[0] + '</span><span  class="text">' + one_text_1[1] + '</span></h3>'
            except:
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h3>'
            new_html.append(one_text)
            continue
        elif item[:6] == "##### ":  # 五级标题
            one_text = item[6:-1]
            try:
                one_text = re.sub('<span class=".*?">', "", one_text)
                one_text = re.sub('</span>', "", one_text)
                one_text = re.sub('<font color.*?>', "", one_text)
                one_text = re.sub('</font>', "", one_text)
                one_text_1 = one_text.split(" ", 1)
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="h3_num">' + \
                        one_text_1[0] + '</span><span  class="text">' + one_text_1[1] + '</span></h3>'
            except:
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h3>'
            new_html.append(one_text)
            continue
        elif item[:7] == "###### ":  # 六级标题
            one_text = item[7:-1]
            try:
                one_text = re.sub('<span class=".*?">', "", one_text)
                one_text = re.sub('</span>', "", one_text)
                one_text = re.sub('<font color.*?>', "", one_text)
                one_text = re.sub('</font>', "", one_text)
                one_text_1 = one_text.split(" ", 1)
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="h3_num">' + \
                        one_text_1[0] + '</span><span  class="text">' + one_text_1[1] + '</span></h3>'
            except:
                one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h3>'
            new_html.append(one_text)
            continue
        else:
            pass

        # 图片
        if item[:2] == "![":  # 图片
            picLink = re.findall('\]\((.*?)\)', item)[0]
            picContent = re.findall('\!\[(.*?)\]\(', item)[0]
            if picContent != "":
                if "@" in picContent:
                    try:  # 这里书写图片的描述@150*150
                        img_size_w = picContent.split('@')[-1].split('*')[0]
                        img_size_h = picContent.split('@')[-1].split('*')[1]
                        one_text = '<img src="' + picLink + '" width="' + img_size_w + '" height="' + img_size_h + '"><span class="img_title">' + \
                                   picContent.split('@')[0] + '</span>'
                        new_html.append(one_text)
                        continue
                    except:
                        pass
                    try:  # 这里书写图片的描述@40%
                        img_size_w = picContent.split('@')[-1]
                        one_text = '<img src="' + picLink + '" width="' + img_size_w + '"><span class="img_title">' + \
                                   picContent.split('@')[0] + "</span>"
                        new_html.append(one_text)
                        continue
                    except:
                        pass
                else:
                    one_text = '<img src="' + picLink + '"><span class="img_title">' + picContent + "</span>"
                    new_html.append(one_text)
                    continue
            else:
                one_text = '<img src="' + picLink + '">'
                new_html.append(one_text)
                continue
        else:
            pass

        # 特殊关键词
        key = "0"
        new_html, key = SpecificKeywords(item[:-1], new_html, keyword_1, keyword_2, keyword_3)  # 函数
        if key == "1":
            continue
        else:
            pass

        # 正文
        if item[:2] != "<p":  # 没有任何标记的正文
            one_text = item[:-1]
            one_text = '<p>' + one_text + "</p>"
            new_html.append(one_text)
        else:
            new_html.append(one_text)

    #加上web尾巴
    one_text = '</span></body></html>'
    new_html.append(one_text)

    new_html = ''.join(new_html) #将new_html转换成str类型

    try: # 找一下css里有没有h1_img,h2_img,h3_img类属性
        h1_img_src = re.findall("h1img:url\((.*?)\);",html_head_style)[0]
        h1_img = '<img class="h1_img" src=' + h1_img_src + '>'
        new_html = re.sub('<img class="h1_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png">',h1_img,new_html)
    except:
        pass
    try:
        h2_img_src = re.findall("h2img:url\((.*?)\);",html_head_style)[0]
        h2_img = '<img class="h2_img" src=' + h2_img_src + '>'
        new_html = re.sub('<img class="h2_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png">', h2_img, new_html)
    except:
        pass
    try:
        h3_img_src = re.findall("h3img:url\((.*?)\);",html_head_style)[0]
        h3_img = '<img class="h3_img" src=' + h3_img_src + '>'
        new_html = re.sub('<img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png">', h3_img, new_html)
    except:
        pass
    try: # 找一下css里有没有h1_svg,h2_svg,h3_svg类属性
        h1_svg_src = re.findall('h1svg:<svg(.*?)</svg>',html_head_style)[0]
        h1_svg = '<svg class="h1_svg" ' + h1_svg_src +'</svg>'
        new_html = re.sub('<svg class="h1_svg"></svg>', h1_svg, new_html)
    except:
        pass
    try: # 找一下css里有没有h1_svg,h2_svg,h3_svg类属性
        h2_svg_src = re.findall("h2svg:<svg(.*?)</svg>",html_head_style)[0]
        h2_svg = '<svg class="h2_svg" ' + h2_svg_src +'</svg>'
        new_html = re.sub('<svg class="h2_svg"></svg>', h2_svg, new_html)
    except:
        pass
    try: # 找一下css里有没有h1_svg,h2_svg,h3_svg类属性
        h3_svg_src = re.findall("h3svg:<svg(.*?)</svg>",html_head_style)[0]
        h3_svg = '<svg class="h3_svg" ' + h3_svg_src +'</svg>'
        new_html = re.sub('<svg class="h3_svg"></svg>', h3_svg, new_html)
    except:
        pass
    WriteFile(new_html, title, html_head_style)
    return "1" # 1表示完成了排版


#以下是幕布转换功能的主要函数
def HtmlConver(up_file_link):#将幕布内容转换成我们css对应的标签
    # 获取css样式
    if item_style == "003":  # css盲盒
        html_head_style = BlindBox()
        if html_head_style == "0":
            return "0" # 0表示icon没有找到
    else:
        with open("./items_css/item_" + item_style + ".html", "r+", encoding="utf-8") as file:
            f1 = file.read()
            html_head_style = re.findall('<textarea rows="35" cols="20" class="out_text" name="textarea" id="item_text" charset="utf-8">([\s\S]*?)</textarea>',f1)[0]

    # 获取用户自定义关键词
    with open("./配置文件.json", "r+", encoding='utf-8') as file:
        json_data = file.read()
        json_data = json.loads(json_data)
    keyword_1 = json_data['keyWords'][0]['name']
    keyword_2 = json_data['keyWords'][1]['name']
    keyword_3 = json_data['keyWords'][2]['name']

    # 获取幕布html
    with open(up_file_link, "r+", encoding="utf-8") as file:
        html = BeautifulSoup(file.read(),'html.parser')

    #转换后html的head
    html_head = '<!DOCTYPE html><html><head><meta charset="utf-8"><style type="text/css">' + html_head_style +'</style><script src="js/left.js" type="text/javascript" charset="utf-8"></script></head><body><span class="body" style="display:block;"><h1></h1>'
    if item_style=="003":#这里有个困难，公众号后台以读取到文字开始拉取，如果文字前有svg图片，不会拉取到
        html_head = '<!DOCTYPE html><html><head><meta charset="utf-8"><style type="text/css">' + html_head_style + '</style><script src="js/left.js" type="text/javascript" charset="utf-8"></script></head><body><span class="body" style="display:block;"><h1></h1><p style="color: #55B494;">图文中部分样式来自www.iconfont.cn，限个人使用</br>icon作者：' + icon_author + '</br>这段话复制到公众号后台可删除</p>'
    else:
        pass

    new_html = []
    new_new_html = []
    new_html.append(html_head)
    new_new_html.append(html_head)

    title = html.find_all('head')[0].title.text  # 拿到标题

    body = html.find_all('body')[0]

    one_list = body.find_all('li')
    mark_ul = 0  # 初始参数
    mark_ol = 0
    mark_bl = 0
    for item in range(20000):
        try:
            new_new_html.append(one_list[item].find_all('div', attrs={"class": "content"})[0].text)
            try:#获取注释中的文本
                new_new_html.append(one_list[item].find_all('div', attrs={"class": "note mm-editor"})[0].text)
            except:
                pass
        except:
            try:
                # new_new_html.append(one_list[item].find_all('img')[0].attrs["src"]) #找图片链接
                find_src = one_list[item].find_all('img')[0].attrs["src"]
            except:
                break
    # print(new_new_html)

    # 进行编码排序
    for item_1 in range(20000):
        try:
            one_list = body.find_all('li')
            one_content = one_list[item_1].find_all('div', attrs={"class": "content"})[0]
            one_word_append = []
            for item_2 in range(50):
                try:
                    onespan = one_content.find_all('span')[item_2]
                    onetext = onespan.text  # 导图中一级标题内容
                    try:  # 文字加粗、斜体、下划线、颜色、超链接
                        tag = onespan.attrs["class"]
                        herf = 0
                        try:  # 获取超链接的地址
                            herf = onespan.parent.attrs["href"]
                        except:
                            pass
                        onetext = DealWord(tag, onetext, herf)  # 转接文字处理
                    except:
                        pass
                    one_word_append.append(onetext)
                except:
                    break

            # 将content内容转换成一个字符串
            one_text = "".join(one_word_append)

            # 引用
            if one_text[:1] == ">":
                if mark_ul == 1:
                    new_html.append("</ul>")
                    mark_ul = 0
                elif mark_ol == 1:
                    new_html.append("</ol>")
                    mark_ol = 0
                else:
                    pass
                bl = '<blockquote data-tool="一陈图文排版">'
                if new_html[len(new_html) - 1][:3] != "<bl" and new_html[len(new_html) - 1][
                                                                :20] != '<p class="citation">':
                    one_text = bl + '<p class="citation">' + one_text[1:] + "</p>"
                    mark_bl = 1
                else:
                    one_text = '<p class="citation">' + one_text[1:] + "</p>"
                    mark_bl = 1
                new_html.append(one_text)
                continue
            elif mark_bl != 0:
                new_html[len(new_html) - 1] = new_html[len(new_html) - 1] + "</blockquote>"
                mark_bl = 0
            else:
                pass

            # 列表
            if one_text[:1] == "-":
                ul = '<ul>'
                if new_html[len(new_html) - 1][:3] != "<ul" and new_html[len(new_html) - 1][:3] != "<li":
                    one_text = ul + "<li>" + one_text[1:] + "</li>"
                    mark_ul = 1
                else:
                    one_text = "<li>" + one_text[1:] + "</li>"
                    mark_ul = 1
                new_html.append(one_text)
                continue
            elif one_text[1:2] == "-" or one_text[2:3] == "-":
                ol = '<ol>'
                if new_html[len(new_html) - 1][:3] != "<ol" and new_html[len(new_html) - 1][:3] != "<li":
                    one_text = ol + "<li>" + one_text[2:] + "</li>"
                    mark_ol = 1
                else:
                    if one_text[1:2] == "-":
                        one_text = "<li>" + one_text[2:] + "</li>"
                    else:
                        one_text = "<li>" + one_text[3:] + "</li>"
                    mark_ol = 1
                new_html.append(one_text)
                continue
            elif mark_ul == 1:
                new_html[len(new_html) - 1] = new_html[len(new_html) - 1] + "</ul>"
                mark_ul = 0
            elif mark_ol == 1:
                new_html[len(new_html) - 1] = new_html[len(new_html) - 1] + "</ol>"
                mark_ol = 0
            else:
                pass

            # 判断内容是否是标题
            try:
                if one_list[item_1].attrs["class"][1] == "heading1":  # 一级标题
                    try:
                        one_text = re.sub('<span class=".*?">', "", one_text)
                        one_text = re.sub('</span>', "", one_text)
                        one_text = re.sub('<font color.*?>', "", one_text)
                        one_text = re.sub('</font>', "", one_text)
                        one_text_1 = one_text.split(" ", 1)
                        one_text = '<h1 data-tool="一陈图文排版" ><img class="h1_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h1_svg_box"><svg class="h1_svg"></svg></span><span class="h1_num">' + one_text_1[
                            0] + '</span><span class="text">' + one_text_1[1] + '</span></h1>'
                    except:
                        one_text = '<h1 data-tool="一陈图文排版" ><img class="h1_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h1_svg_box"><svg class="h1_svg"></svg></span><span  class="text_noNum">' + one_text + '</span></h1>'
                    new_html.append(one_text)
                    continue
                else:
                    pass
                if one_list[item_1].attrs["class"][1] == "heading2":  # 二级标题
                    try:
                        one_text = re.sub('<span class=".*?">', "", one_text)
                        one_text = re.sub('</span>', "", one_text)
                        one_text = re.sub('<font color.*?>', "", one_text)
                        one_text = re.sub('</font>', "", one_text)
                        one_text_1 = one_text.split(" ", 1)
                        one_text = '<h2 data-tool="一陈图文排版" ><img class="h2_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h2_svg_box"><svg class="h2_svg"></svg></span><span class="h2_num">' + one_text_1[
                            0] + '</span><span  class="text">' + one_text_1[1] + '</span></h2>'
                    except:
                        one_text = '<h2 data-tool="一陈图文排版" ><img class="h2_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h2_svg_box"><svg class="h2_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h2>'
                    new_html.append(one_text)
                    continue
                else:
                    pass
                if one_list[item_1].attrs["class"][1] == "heading3":  # 三级标题
                    try:
                        one_text = re.sub('<span class=".*?">', "", one_text)
                        one_text = re.sub('</span>', "", one_text)
                        one_text = re.sub('<font color.*?>', "", one_text)
                        one_text = re.sub('</font>', "", one_text)
                        one_text_1 = one_text.split(" ", 1)
                        one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="h3_num">' + one_text_1[
                            0] + '</span><span  class="text">' + one_text_1[1] + '</span></h3>'
                    except:
                        one_text = '<h3 data-tool="一陈图文排版" ><img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png"><span class="h3_svg_box"><svg class="h3_svg"></svg></span><span class="text_noNum">' + one_text + '</span></h3>'

                    new_html.append(one_text)
                    continue
                else:
                    pass
            except:
                pass

            # 其他特定的关键词样式
            key = "0"
            new_html,key = SpecificKeywords(one_text,new_html,keyword_1,keyword_2,keyword_3) # 函数
            if key == "1":
                continue
            else:
                pass
            if one_text[:2] != "<p":  # 没有任何标记的正文
                one_text = '<p>' + one_text + "</p>"
                new_html.append(one_text)
            else:
                new_html.append(one_text)
            try:#获取注释中的文本
                one_content_notes = one_list[item_1].find_all('div', attrs={"class": "note mm-editor"})[0]
                one_word_append = []
                for item_2 in range(50):
                    try:
                        onespan_notes = one_content_notes.find_all('span')[item_2]
                        onetext_notes = onespan_notes.text
                        try:  # 文字加粗、斜体、下划线、颜色、超链接
                            tag = onespan_notes.attrs["class"]
                            herf = 0
                            try:  # 获取超链接的地址
                                herf = onespan_notes.parent.attrs["href"]
                            except:
                                pass
                            onetext_notes = DealWord(tag, onetext_notes, herf)  # 转接文字处理
                        except:
                            pass
                        one_word_append.append(onetext_notes)
                    except:
                        break
                # 将content内容转换成一个字符串
                one_text = "".join(one_word_append)
                one_text = '<blockquote data-tool="一陈图文排版"><p class="citation">' + one_text + "</p></blockquote>"
                new_html.append(one_text)
            except:
                pass
        except:
            try:  # 图片
                if new_new_html[len(new_html) - 1] != "":
                    if "@" in new_new_html[len(new_html) - 1]:
                        try:  # 这里书写图片的描述@150*150
                            img_size_w = new_new_html[len(new_html) - 1].split('@')[-1].split('*')[0]
                            img_size_h = new_new_html[len(new_html) - 1].split('@')[-1].split('*')[1]
                            img = one_list[item_1].find_all('img')[0].attrs['src']
                            one_text = '<img src="' + img + '" width="' + img_size_w + '" height="' + img_size_h + '"><span class="img_title">' + new_new_html[len(new_html) - 1].split('@')[0] + '</span>'
                            new_html[len(new_html) - 1] = one_text
                            continue
                        except:
                            pass
                        try:  # 这里书写图片的描述@40%
                            img_size_w = new_new_html[len(new_html) - 1].split('@')[-1]
                            img = one_list[item_1].find_all('img')[0].attrs['src']
                            one_text = '<img src="' + img + '" width="' + img_size_w + '"><span class="img_title">' + new_new_html[len(new_html) - 1].split('@')[0] + "</span>"
                            new_html[len(new_html) - 1] = one_text
                            continue
                        except:
                            pass
                    else:
                        img = one_list[item_1].find_all('img')[0].attrs['src']
                        one_text = '<img src="' + img + '"><span class="img_title">' + new_new_html[len(new_html) - 1] + "</span>"
                        new_html[len(new_html) - 1] = one_text
                        continue
                else:
                    img = one_list[item_1].find_all('img')[0].attrs['src']
                    one_text = '<img src="' + img + '">'
                    new_html[len(new_html) - 1] = one_text
                    continue
            except:
                one_text = '</span></body></html>'
                new_html.append(one_text)
                break

    # print(new_html)
    new_html = ''.join(new_html) #将new_html转换成str类型

    try: # 找一下css里有没有h1_img,h2_img,h3_img类属性
        h1_img_src = re.findall("h1img:url\((.*?)\);",html_head_style)[0]
        h1_img = '<img class="h1_img" src=' + h1_img_src + '>'
        new_html = re.sub('<img class="h1_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png">',h1_img,new_html)
    except:
        pass
    try:
        h2_img_src = re.findall("h2img:url\((.*?)\);",html_head_style)[0]
        h2_img = '<img class="h2_img" src=' + h2_img_src + '>'
        new_html = re.sub('<img class="h2_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png">', h2_img, new_html)
    except:
        pass
    try:
        h3_img_src = re.findall("h3img:url\((.*?)\);",html_head_style)[0]
        h3_img = '<img class="h3_img" src=' + h3_img_src + '>'
        new_html = re.sub('<img class="h3_img" src="https://re-yichen.oss-cn-beijing.aliyuncs.com/img/%E6%9C%AA%E6%A0%87%E9%A2%98-1.png">', h3_img, new_html)
    except:
        pass
    try: # 找一下css里有没有h1_svg,h2_svg,h3_svg类属性
        h1_svg_src = re.findall('h1svg:<svg(.*?)</svg>',html_head_style)[0]
        h1_svg = '<svg class="h1_svg" ' + h1_svg_src +'</svg>'
        new_html = re.sub('<svg class="h1_svg"></svg>', h1_svg, new_html)
    except:
        pass
    try: # 找一下css里有没有h1_svg,h2_svg,h3_svg类属性
        h2_svg_src = re.findall("h2svg:<svg(.*?)</svg>",html_head_style)[0]
        h2_svg = '<svg class="h2_svg" ' + h2_svg_src +'</svg>'
        new_html = re.sub('<svg class="h2_svg"></svg>', h2_svg, new_html)
    except:
        pass
    try: # 找一下css里有没有h1_svg,h2_svg,h3_svg类属性
        h3_svg_src = re.findall("h3svg:<svg(.*?)</svg>",html_head_style)[0]
        h3_svg = '<svg class="h3_svg" ' + h3_svg_src +'</svg>'
        new_html = re.sub('<svg class="h3_svg"></svg>', h3_svg, new_html)
    except:
        pass
    WriteFile(new_html, title, html_head_style)
    return "1" # 1表示完成了排版

def DealWord(tag, onetext, herf=''): #文字处理
    if tag[0] == "bold": #加粗
        onetext = '<span class="strong">' + onetext + '</span>'
    elif tag[0] == "italic": #斜体
        onetext = '<span class="italics">' + onetext + '</span>'
    elif tag[0] == "underline": #下划线
        onetext = '<span class="underline">' + onetext + "</span>"
    elif tag[0] == "codespan": #高亮
        onetext = '<span class="codespan">' + onetext + "</span>"
    elif tag[0] == "text-color-red": #颜色-红
        onetext ="<font color=#dc2d1e>" + onetext + "</font>"
    elif tag[0] == "text-color-yellow": #颜色-黄
        onetext ="<font color=#ffaf38>" + onetext + "</font>"
    elif tag[0] == "text-color-green": #颜色-绿
        onetext ="<font color=#75c940>" + onetext + "</font>"
    elif tag[0] == "text-color-blue": #颜色-蓝
        onetext ="<font color=#3da8f5>" + onetext + "</font>"
    elif tag[0] == "text-color-purple": #颜色-紫
        onetext ="<font color=#797ec9>" + onetext + "</font>"
    elif tag[0] == "content-link-text": #超链接，使用下划线样式
        onetext ='<span class="underline">' + onetext +'</span>'
    else:
        pass
    return onetext

# 保存排版文件
def WriteFile(new_html,title,html_head_style):
    # 如果路径不存在就创建，如果不存在就不创建
    if not os.path.exists('./历史排版'):
        os.mkdir('./历史排版')
    global title_name
    title_name = re.sub("[\?\(\)\（\）\!\%\[\]\,\。\？\.]", "", title)
    with open("./历史排版/"+title_name+".html","w",encoding='utf-8') as file:
        file.writelines(new_html)
        file.close()
    with open("./left.html","w+",encoding='utf-8') as file:
        file.writelines(new_html)
        file.close()
    if item_style=='003':
        with open("./items_css/right.html", "r+", encoding='utf-8') as file:
            f1 = file.read()
            css = '<textarea rows="35" cols="20" class="out_text" name="textarea" id="item_text" charset="utf-8">'+ html_head_style +'</textarea>'
            f1 = re.sub('<textarea rows="35" cols="20" class="out_text" name="textarea" id="item_text" charset="utf-8">([\s\S]*?)</textarea>',css,f1)
        with open("./items_css/right.html", "w+", encoding='utf-8') as file:
            file.writelines(f1)
            file.close()

# 转换时各样式特殊关键词
def SpecificKeywords(one_text,new_html,keyword_1,keyword_2,keyword_3):
    if one_text == "***" or one_text == "---" or one_text == "___":
        if item_style == '003':
            one_text = '<span class="divider"></span><span class="divider_box"><svg class="divider_img" style="display:inline-block;width: 30px; height: 30px;' + img_divider[48:] + '</span>'
            new_html.append(one_text)
            return new_html, "1"
        else:
            num = Item_styleToNum() #先做判断再运行，提高效率
            with open("./配置文件.json", "r+", encoding='utf-8') as file:
                json_data = file.read()
                json_data = json.loads(json_data)
            img = json_data['divider'][num]['url']
            one_text = '<span class="divider"></span><img class="divider_img" src="' + img + '" >'
            new_html.append(one_text)
            return new_html, "1"
    elif one_text == keyword_1:
        with open("./配置文件.json", "r+", encoding='utf-8') as file:
            json_data = file.read()
            json_data = json.loads(json_data)
        one_text = json_data['keyWords'][0]['html']
        new_html.append(one_text)
        return new_html, "1"
    elif one_text == keyword_2:
        with open("./配置文件.json", "r+", encoding='utf-8') as file:
            json_data = file.read()
            json_data = json.loads(json_data)
        one_text = json_data['keyWords'][1]['html']
        new_html.append(one_text)
        return new_html, "1"
    elif one_text == keyword_3:
        with open("./配置文件.json", "r+", encoding='utf-8') as file:
            json_data = file.read()
            json_data = json.loads(json_data)
        one_text = json_data['keyWords'][2]['html']
        new_html.append(one_text)
        return new_html, "1"
    else:
        return new_html, "0"

# 选择样式时替换各样式中的分割线
def ReplaceKeywordStyle(f2):
    try:
        num = Item_styleToNum()
        with open("./配置文件.json","r+",encoding='utf-8') as file:
            json_data = file.read()
            json_data = json.loads(json_data)
        img_divider = '<span class="divider"></span><img class="divider_img" src="'+ json_data['divider'][num]['url'] +'" >'
        f2 = re.sub('<span class="divider"></span><img class="divider_img" src=".*?" >', img_divider, f2)
        return f2
    except:
        return f2

def Item_styleToNum(): # 样式与json序列中列表对应
    if item_style == "1":
        num = 0
    elif item_style == "2":
        num = 1
    elif item_style == "3":
        num = 2
    elif item_style == "4":
        num = 3
    elif item_style == "5":
        num = 4
    elif item_style == "6":
        num = 5
    elif item_style == "7":
        num = 6
    elif item_style == "8":
        num = 7
    elif item_style == "001":
        num = 8
    elif item_style == "002":
        num = 9
    return num

# css样式盲盒
def BlindBox():
    global img_divider
    global icon_author
    with open("./配置文件.json", "r+", encoding="utf-8") as file:
        f1 = file.read()
        f1 = json.loads(f1)
        keyword = str(f1['keyWords'][3]['name'])
        print(keyword)
    for item in range(10):  # 出错了就多找几次
        try:
            if keyword == "":
                # print("盲盒无指定关键词")
                pageRandom = random.randint(1, 333)  # 页码随机数
                iconGroupRandom = random.randint(0, 8)  # 一个页面内icon组随机,一个页面有9个icon组

                url = 'https://www.iconfont.cn/api/collections.json?type=2&sort=time&limit=9&page=' + str(pageRandom)
                html = requests.get(url).content.decode('utf-8')
                html = json.loads(html)
                icons_count = html['data']['lists'][iconGroupRandom]['icons_count']
                while icons_count < 4:  # 因为至少需要4个svg图像，小于4的icon组不考虑
                    iconGroupRandom = random.randint(0, 8)
                    icons_count = html['data']['lists'][iconGroupRandom]['icons_count']
            else:
                url = 'https://www.iconfont.cn/api/collections.json?type=2&limit=20&keyword=' + str(keyword)
                html = requests.get(url).content.decode('utf-8')
                html = json.loads(html)
                iconsGroup_count = html['data']['count']  # 确定找到的icon组的数量
                if iconsGroup_count == 0:
                    # print("该关键词没有icon")
                    return "0"  # 0表示排版未完成
                elif iconsGroup_count > 20:
                    iconGroupRandom = random.randint(0, 20)
                else:
                    iconGroupRandom = random.randint(0, iconsGroup_count - 1)
                icons_count = html['data']['lists'][iconGroupRandom]['icons_count']
                i = 0
                while icons_count < 4 or i > 5:  # 因为至少需要4个svg图像，小于4的icon组不考虑
                    if iconsGroup_count > 20:
                        iconGroupRandom = random.randint(0, 20)
                    else:
                        iconGroupRandom = random.randint(0, iconsGroup_count - 1)
                    icons_count = html['data']['lists'][iconGroupRandom]['icons_count']
                    i = i + 1

            icon_url = "https://www.iconfont.cn/api/collection/detail.json?id=" + str(
                html['data']['lists'][iconGroupRandom]['id'])
            icon_content = requests.get(icon_url).content.decode('utf-8')
            icon_content = json.loads(icon_content)
            icon_author = icon_content['data']['creator']['nickname']  # 作者的名字

            # 第一个svg图标
            iconRandom_1 = random.randint(0, icons_count - 1)  # 进入内部页面随机选择icon
            icon_1 = icon_content['data']['icons'][iconRandom_1]['show_svg']

            # 第二个svg图标
            iconRandom_2 = random.randint(0, icons_count - 1)  # 进入内部页面随机选择icon
            while iconRandom_2 == iconRandom_1:
                iconRandom_2 = random.randint(0, icons_count - 1)
            icon_2 = icon_content['data']['icons'][iconRandom_2]['show_svg']

            # 第三个svg图标
            iconRandom_3 = random.randint(0, icons_count - 1)  # 进入内部页面随机选择icon
            while iconRandom_3 == iconRandom_1 or iconRandom_3 == iconRandom_2:
                iconRandom_3 = random.randint(0, icons_count - 1)
            icon_3 = icon_content['data']['icons'][iconRandom_3]['show_svg']

            # 第四个svg图标
            iconRandom_4 = random.randint(0, icons_count - 1)  # 进入内部页面随机选择icon
            while iconRandom_4 == iconRandom_1 or iconRandom_4 == iconRandom_2 or iconRandom_4 == iconRandom_3:
                iconRandom_4 = random.randint(0, icons_count - 1)
            icon_4 = icon_content['data']['icons'][iconRandom_4]['show_svg']

            # 找颜色
            icon_soup_1 = BeautifulSoup(icon_1, 'html.parser')
            # 找第一个颜色
            icon_color1 = icon_soup_1.find_all("path")[0]['fill']
            try:  # 找第二个颜色
                icon_color2 = icon_soup_1.find_all("path")[1]['fill']
                if icon_color2 == icon_color1 or icon_color2 == "#FFFFFF":
                    try:
                        icon_color2 = icon_soup_1.find_all("path")[2]['fill']
                    except:
                        icon_color2 = icon_color1
                else:
                    pass
            except:
                icon_color2 = icon_color1
            if icon_color1 == "#FFFFFF":
                icon_color1 = icon_color2
            break
        except:
            continue

    # print(str(icons_count) + "---" + str(iconRandom_1) + "---" + str(iconRandom_2) + "---" + str(
    #     iconRandom_3) + "---" + str(iconRandom_4))
    # print(icon_url)
    # print(icon_author)
    # print(icon_1, icon_2, icon_3, icon_4)
    # print(icon_color1, icon_color2)
    try:
        color_1 = icon_color1 # 主题色
        color_2 = icon_color2 # 辅色
        img_divider = icon_4 # 分割线样式
        border_a = '''border-left: '''+str(random.randint(0,3))+'''px '''+random.choice(['dotted','dashed','solid','double'])+''' '''+random.choice([color_1,color_2])+''';
    border-radius: 0px 0px '''+str(random.randint(0,20))+'''px 0px;'''
        border_b = '''border-style: solid;
                border: '''+str(random.randint(1,3))+'''px '''+random.choice(['dotted','dashed','solid','double'])+''' '''+random.choice([color_1,color_2])+''';
                border-radius: '''+str(random.randint(0,10))+'''px;
                '''
        html_head_style = '''
.body{/* 整个页面属性 */
    padding: 0 10px; /* 整体页面边距:上下0,左右10px */
    font-size: 16px;/* 文字大小 */
    color: #3f3f3f;/* 文字颜色 */
    text-align: left; /* 文字居左 */
    text-align: justify;/* 文字两端对齐 */
    line-height: 1.6em;/* 行高 */
    letter-spacing: 0.034em;/* 字符间隔 */
    word-wrap: break-word; /* 允许长单词换行到下一行 */
    font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, 'PingFang SC', Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;/* 字体 */
}
h1{/* 一级标题框架属性 */
    letter-spacing: 0.544px;
    white-space: normal;
    font-size: 24px;
    font-weight: bold;
    color: black;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 25px;
}
h1 .h1_svg_box{
    display:block;
    margin-bottom:0px;
}
h1 .h1_svg{
    display:block;
    margin:5px auto;
    h1svg:<svg class="icon" style="width: 50px; height: 50px;'''+ icon_1[48:] +''';
}
h1 .h1_num{/* 一级标题序号属性 */
    font-size: 16px;
    display: inline-block;
    text-align: center;
    color: white;
    border-bottom: 2px solid '''+color_2+''';
    background-color: '''+color_1+''';
    padding:2px 4px 0px;
}
h1 .text{/* 一级标题文字属性 */
    font-size: 16px;
    display: inline-block;
    text-align: center;
    color: white;
    border-bottom: 2px solid  '''+color_2+''';
    background-color:  '''+color_1+''';
    padding:2px 4px 0px;
}
h1 .text_noNum{/* 一级标题文字属性（无序号） */
    font-size: 16px;
    color: white;
    border-bottom: 2px solid  '''+color_2+''';
    background-color:  '''+color_1+''';
    padding:2px 4px 0px;
}
h2{/* 二级标题框架属性 */
    display: block;
    padding: 0px;
    font-weight: bold;
    color: black;
    font-size: 22px;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 25px;
}
h2 .h2_svg_box{
    display:block;
    margin-bottom:0px;
}
h2 .h2_svg{
    display:block;
    margin:5px auto;
    h2svg:<svg class="icon" style="width: 40px; height: 40px;'''+ icon_2[48:] +''';
}
h2 .h2_num{/* 二级标题序号属性 */
    display: inline-block;
    text-align: center;
    height: 38px; 
    line-height: 42px; 
    color:  '''+color_1+'''; 
    font-size: 16px; 
    margin-bottom: 10px;
    margin-right: 5px;
}
h2 .text{/* 二级标题文字属性 */
    display: inline-block;
    text-align: center;
    height: 38px; 
    line-height: 42px; 
    color:  '''+color_1+'''; 
    font-size: 16px; 
    margin-bottom: 10px;
}
h2 .text_noNum{/* 二级标题文字属性（无序号） */
    display: inline-block;
    text-align: center;
    height: 38px; 
    line-height: 42px; 
    color:  '''+color_1+'''; 
    font-size: 16px; 
    margin-bottom: 10px;
}
h3{/* 三级标题框架属性 */
    margin: 30px 0px 10px;
}
h3 .h3_svg_box{
    display:inline-block;
}
h3 .h3_svg{
    display:block;
    position: relative;
    top: 6px;
    h3svg:<svg class="icon" style="margin-top: -5px; width: 25px; height: 25px;'''+ icon_3[48:] +''';
}
h3 .h3_num{/* 三级标题序号属性 */
    font-size: 16px;
    font-weight: bold;
    display: inline-block;
    color:  '''+color_2+''';
    margin-left:5px;
    margin-right: 5px;
}
h3 .text{/* 三级标题文字属性 */
    font-size: 16px;
    font-weight: bold;
    display: inline-block;
    color:  '''+color_2+''';
}
h3 .text_noNum{/* 三级标题文字属性（无序号） */
    font-size: 16px;
    font-weight: bold;
    display: inline-block;
    color:  '''+color_2+''';
    margin-left:5px;
}
p{/* 正文属性 */
    margin: 10px 0px;
    /* text-indent:2em */ /* 首行缩进 */
}
img{/* 图片属性 */
    display: block;
    margin: 20px auto 10px;
    max-width: 100%;
    border-radius: '''+str(random.randint(0,10))+'''px;
}
.img_title{/* 图片名称 */
    display: block;
    margin-bottom: 20px;
    text-align: center;
    color: #888;
    font-size: '''+str(random.randint(12,14))+'''px;
}
.underline,.codespan{/* 下划线属性 */
    font-size: 14px;
    font-family: Operator Mono, Consolas, Monaco, Menlo, monospace;
    margin: 0 2px;
    padding: 2px 4px;
    border-radius: 4px;
    color: '''+color_1+''';
    background-color: rgba(27,31,35,.05);
    word-wrap: break-word;
    word-break: break-all;
}
.strong{/* 加粗属性 */
    font-weight: bold;
    line-height: 1.75em;
    color: '''+random.choice([color_1,color_2])+''';
}
.italics{/* 斜体属性 */
    background: linear-gradient(to right, '''+random.choice([color_1,color_2])+''', '''+random.choice([color_1,color_2])+''');
    color: white;
    border-width: 0.25em 0px;
    padding: 2px 4px;
}
ul{/* 无序列表框架 */
    margin-top: 8px;
    margin-bottom: 8px;
    padding-left: 20px;
    color: black;
    list-style-type: '''+random.choice(['disc','circle','square'])+''';
}
ul li{/* 无序列表文字 */
    margin-top: 5px;
    margin-bottom: 5px;
    line-height: 26px;
    text-align: left;
    color: rgb(1,1,1);
}
ol{/* 有序列表框架 */
    margin-top: 8px;
    margin-bottom: 8px;
    padding-left: 30px;
    color: black;
    list-style-type: '''+random.choice(['decimal','decimal-leading-zero','lower-roman','upper-roman','lower-alpha','upper-alpha'])+''';
}
ol li{/* 有序列表文字 */
    margin-top: 5px;
    margin-bottom: 5px;
    line-height: 26px;
    text-align: left;
    color: rgb(1,1,1);
}
blockquote{/* 引用框架 */
    display: block;
    font-size: 0.9em;
    color: #6a737d;
    overflow: auto;
    overflow-scrolling: touch;
    background: rgba(0, 0, 0, 0.05);
    background-color: #FBF9FD;
    margin: 20px 0px;
    padding: 15px 20px;
    line-height: 27px;
    '''+random.choice([border_a,border_b])+'''
}
blockquote p{/* 引用内容 */
    margin: 0px;
    padding: 0px;
    line-height: 26px;
    font-size: 15px;
    color: rgb(89,89,89);
}
.divider{/* 分割线属性 */
    display: block;
}
.divider_box{/* 包裹分割线图片的span标签属性 */
    display: block;
    margin-top: 50px;
    text-align: '''+random.choice(['center','right'])+''';
    margin-bottom: 80px;
    border-bottom:1px '''+random.choice(['dotted','dashed','solid','double'])+''' '''+random.choice([color_1,color_2])+''' ;
}
.divider_img{/* 分割线图片属性 */
    display: block;
}

body{ /* 默认属性 */
    padding:0px 0px;
    margin:0px;
    background-color: white;/* 背景颜色 */
}
svg{ /* 默认属性，需要添加svg图像时可使用 */
    display:none;
}
.h1_img,.h2_img,.h3_img{ /* 默认属性，需要添加图片标题背景时可使用 */
    display:none;
}
    '''
        return html_head_style
    except:
        return "0"