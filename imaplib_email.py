#-*- encoding: utf-8 -*-
#author : rayment
#CreateDate : 2013-01-24

import os
import imaplib
import email
#设置命令窗口输出使用中文编码
import sys
reload(sys)
sys.setdefaultencoding('gbk')

#保存文件方法（都是保存在指定的根目录下）
def savefile(filename, data, path, attachment_path=""):
    try:
        filepath = path + attachment_path
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        print 'Saved as ' + filepath
        filepath = filepath + filename
        with open(filepath, 'wb') as f:
            f.write(data)
    except Exception as e:
        print('filename error', e)
        f.close()
   
#字符编码转换方法
def my_unicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)

#获得字符编码方法
def get_charset(message, default="ascii"):
    #Get the message charset
    return message.get_charset()

#解析邮件方法（区分出正文与附件）
def parseEmail(msg, mypath):
    mailContent = None
    contenttype = None
    suffix =None
    for part in msg.walk():
        if not part.is_multipart():
            contenttype = part.get_content_type()   
            filename = part.get_filename()
            charset = get_charset(part)
            #是否有附件
            if filename:
                h = email.Header.Header(filename)
                dh = email.Header.decode_header(h)
                fname = dh[0][0]
                encodeStr = dh[0][1]
                if encodeStr != None:
                    if charset == None:
                        fname = fname.decode(encodeStr, 'gbk')
                    else:
                        fname = fname.decode(encodeStr, charset)
                data = part.get_payload(decode=True)
                print('Attachment : ' + fname)
                #保存附件
                if fname != None or fname != '':
                    print 'fname *', fname
                    fname = "xiaoying.xlsx"
                    savefile(fname, data, mypath, "/attachment_file/")            
            else:
                if contenttype in ['text/plain']:
                    suffix = '.txt'
                if contenttype in ['text/html']:
                    suffix = '.htm'
                if charset == None:
                    mailContent = part.get_payload(decode=True)
                else:
                    mailContent = part.get_payload(decode=True).decode(charset)         
    return  (mailContent, suffix)

#获取邮件方法
def getMail(mailhost, account, password, store_path):
    imapServer = imaplib.IMAP4(mailhost)
    imapServer.login(account, password)
    imapServer.select()
    #邮件状态设置，新邮件为Unseen
    #Message statues = 'All,Unseen,Seen,Recent,Answered, Flagged'
    resp, items = imapServer.search(None, "Unseen")
    # resp, items = imapServer.search(None, "seen")
    print "items", items
    number = 1
    for i in items[0].split():
       #get information of email
       resp, mailData = imapServer.fetch(i, "(RFC822)")   
       mailText = mailData[0][1]
       msg = email.message_from_string(mailText)
       ls = msg["From"].split(' ')
       strfrom = ''
       if(len(ls) == 2):
           fromname = email.Header.decode_header((ls[0]).strip('\"'))
           strfrom = 'From : ' + my_unicode(fromname[0][0], fromname[0][1]) + ls[1]
       else:
           strfrom = 'From : ' + msg["From"]
       strdate = 'Date : ' + msg["Date"]
       subject = email.Header.decode_header(msg["Subject"])
       sub = my_unicode(subject[0][0], subject[0][1])
       strsub = 'Subject : ' + sub
             
       mailContent, suffix = parseEmail(msg, mypath)
       #命令窗体输出邮件基本信息
       print '\n'
       print 'No : ' + str(number)
       print strfrom
       print strdate
       print strsub
       '''
       print 'Content:'
       print mailContent
       '''
       #保存邮件正文
       if (suffix != None and suffix != '') and (mailContent != None and mailContent != ''):
           print "save file ", str(number) + suffix
           savefile(str(number) + suffix, mailContent, mypath)
           number = number + 1
           
    imapServer.close()
    imapServer.logout()


if __name__ =="__main__":
    #邮件保存
    mypath = './static/emails'
    print 'begin to get email...'
    getMail('imap.xxxxx.xxx', 'xxxxx@xxxxx.xxx', 'xxxx', mypath)
    #126邮箱登陆没用ssl
    #getMail('imap.126.com', 'xxxxxxxxx@126.com', 'xxxxxxxxxx', mypath, 143, 0)
    print 'the end of get email.'
