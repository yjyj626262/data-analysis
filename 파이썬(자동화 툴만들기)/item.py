import cx_Oracle as cx

conn = cx.connect("scott", "1234", "localhost:1521/xe")
cursor = conn.cursor()

# 상품번호에 해당하는 수량 반환함수
def invol(itname):
    sql = 'select it_vol from it_oracle where it_name = :1'
    cursor.execute(sql, [itname])
    itvol = cursor.fetchone()
    return itvol[0]

# 상품번호로 상품이름 반환
def itname(itno):
    sql = "SELECT it_name FROM it_oracle WHERE it_no = :1"
    cursor.execute(sql, [itno])
    itname = cursor.fetchone()
    return itname

# 상품정보수정
## 고객이 결제한 만큼 값을 수정을 한다.
def itupdate(itname, invol2):
    itvol = invol(itname)
    itvol = itvol-invol2
    sql = "update it_oracle set it_vol = :1 where it_name = :2"
    cursor.execute(sql, [itvol, itname])   

def ad_itupdate():
    it_no = int(input('몇번의 상품을 변경하시겠습니까?'))
    it_name = input('수정하실 상품명을 입력하세요 : ')
    it_price = int(input('수정하실 상품 가격을 입력하세요 : '))
    it_vol = int(input('수정하실 수량을 입력하세요 : '))
    sql = "update it_oracle set it_name = :1, it_price = :2, it_vol = :3 where it_no = :4"
    cursor.execute(sql, [it_name, it_price, it_vol, it_no])
    print("상품정보가 수정되었습니다.")         

def ad_itdelete():
    itno = int(input('몇번의 상품을 삭제하시겠습니까?'))
    sql = 'delete from it_oracle where it_no = :1'
    cursor.execute(sql, [itno])
    print(f'{itno}번의 상품이 삭제되었습니다.')

# 상품정보조회
def listItemall():
    cursor.execute("select * from it_oracle")
    rs = cursor.fetchall()
    if len(rs) == 0:
        print("등록된 상품정보가 존재하지 않습니다.")
    else:
        for row in rs:
            print(row)

def listItem():
    cursor.execute("select it_name, it_price, it_vol from it_oracle")
    rs = cursor.fetchall()
    if len(rs) == 0:
        print("등록된 상품정보가 존재하지 않습니다.")
    else:
        for row in rs:
            print(row)

            
            
# 상품등록
def initem():
    itname = input('추가하실 상품명을 입력하세요 : ')
    itprice = int(input('추가하실 상품 가격을 입력하세요 : '))
    itvol = int(input('수량을 입력하세요 : '))
    sql = "INSERT INTO it_oracle (it_no, it_name, it_price, it_vol) VALUES (it_seq.NEXTVAL, :1, :2, :3)"
    cursor.execute(sql, [itname, itprice, itvol])
    print("상품등록이 완료되었습니다.")