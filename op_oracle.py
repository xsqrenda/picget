import cx_Oracle,os

def wr_beauty(uid,keyword,url,title):
    try:
        os.environ['NLS_LANG'] = "SIMPLIFIED CHINESE_CHINA.AL32UTF8" #设置Oracle语言编码变量，非常重要
        db = cx_Oracle.connect('hr/112510@39.104.235.35:49161/xe')
        cursor = db.cursor()
        param={'id':uid,'keyword':keyword,'url':url,'title':title}
        sql="""insert into HR."beauty" values(:id,:keyword,:url,:title)"""
        cursor.execute(sql,param)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        raise e
