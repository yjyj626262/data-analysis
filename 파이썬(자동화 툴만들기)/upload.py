## 오라클 연동
import cx_Oracle as cx
conn = cx.connect('scott','1234','localhost:1521/xe')
cursor=conn.cursor()

## user 계정 오라클 연동
cursor.execute('select * from us_oracle')

## uslist를 us_id를 key값으로 관리
for row in cursor :
    us_id = row[0]
    us_info = {
        'us_id' : row[0],
        'us_pw' : row[1],
        'us_name' : row[2]
    }
    uslist[us_id] = us_info
cursor.close()
conn.close()