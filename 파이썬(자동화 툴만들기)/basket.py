import cx_Oracle as cx

conn = cx.connect("scott", "1234", "localhost:1521/xe")
cursor = conn.cursor()

# 장바구니 전체 목록 확인
def bk_viewall() :
    cursor.execute("select * from bk_oracle")
    rs = cursor.fetchall()
    
    if len(rs) == 0:
        print("등록된 상품정보가 존재하지 않습니다.")
    else:
        for row in rs:
            print(row)

# 사용자의 장바구니 확인
def bk_view(userid):
    sql = "select * from bk_oracle where user_id = :1"
    cursor.execute(sql, [userid])
    rs = cursor.fetchall()
    
    if len(rs) == 0:
        print("등록된 상품정보가 존재하지 않습니다.")
    else:
        for row in rs:
            print(row)
    
# 장바구니에 담을 물품가격을 이름으로 조회
def bk_price(itname):
    sql = 'select it_price from it_oracle where it_name = :1'
    cursor.execute(sql, [itname])  
    itprice = cursor.fetchone()  
    return itprice[0]
    
# 장바구니에 물품등록
def bk_insert(userid, itname, itprice, itvol):
    sql = "insert into bk_oracle values(:1, :2, :3, :4)"
    cursor.execute(sql, [userid, itname, itprice, itvol])  
    print("상품등록이 완료되었습니다.")
    
# 장바구니 수량조회
def bk_checkvol(userid, itname):
    sql = 'select it_vol from bk_oracle where user_id = :1 and it_name = :2'
    cursor.execute(sql, [userid, itname])
    bkvol = cursor.fetchone()
    return bkvol[0]

# 장바구니 수량조절
def bk_vol(userid, itname):
    add = int(input('몇개 추가 하실 것 입니까?(제거는 -사용) : '))
    itvol = bk_checkvol(userid, itname) + add
    if itvol >= 0 :
        sql = "update bk_oracle set it_vol = :1 where user_id = :2 and it_name = :3"
        cursor.execute(sql, [itvol, userid, itname])
        conn.commit()
        print("장바구니가 수정되었습니다.")
        bk_view(userid)
        if itvol == 0 :
            sql = 'DELETE FROM bk_oracle WHERE it_vol = :1'
            cursor.execute(sql, [itvol])
            return
        return
    else :
        print('해당 수량만큼 존재하지 않습니다.')
        
# 결제하고 나서 장바구니 수량 수정
def bk_update(userid, itname, invol):
    itvol = bk_checkvol(userid, itname) -invol
    sql = "update bk_oracle set it_vol = :1 where it_name = :2 and user_id = :3"
    cursor.execute(sql, [itvol, itname, userid])
    if itvol == 0 :
        sql = 'DELETE FROM bk_oracle WHERE it_vol = :1'
        cursor.execute(sql, [itvol])

def bkvol_update():
    sql = 'DELETE FROM bk_oracle where it_vol = 0'
    cursor.execute(sql)
    conn.commit()
        
def itvol_update():
    sql = "update it_oracle set it_vol = '품절' where it_vol = 0"
    cursor.execute(sql)
        
def update():
    bkvol_update()
    itvol_update()
    
    
    
    
    
    