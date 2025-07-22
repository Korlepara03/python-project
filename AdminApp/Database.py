import pymysql
def DBConnection():
    con=pymysql.connect(host='localhost', user='root', password='root', database='book_recommend', charset='utf8')
    return con
