import cx_Oracle as cx

conn = cx.connect("scott", "1234", "localhost:1521/xe")
cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()



# 키보드로 회원 값 받기
def insertpn():
    a = input('비밀번호를 입력하세요 : ')
    b = input('이름을 입력하세요 : ')
    return a, b


def insertkey():
    a = input('id를 입력하세요 : ')
    b = input('비밀번호를 입력하세요 : ')
    return a, b

def insertall():
    a, b = insertkey()
    c = input('이름을 입력하세요 : ')
    return a, b, c

# 회원 등록
def insert(userid, userpass, username):
    sql = "insert into us_oracle values(:1, :2, :3, 0, 'vip0')"  # us_money 값을 0으로 초기화
    cursor.execute(sql, [userid, userpass, username])
    print("회원등록이 완료되었습니다.")

        
# 회원정보수정
## 회원아이디가 일치하는 사람에 한하여 수정을 한다.
def update(userid, userpass, username):
    sql = "update us_oracle set us_pw = :1, us_name = :2 where us_id = :3"
    cursor.execute(sql, [userpass, username, userid])
    print("회원정보가 수정되었습니다.")   
        
## 회원탈퇴
def delete(userid, userpass):
    sql = "DELETE FROM us_oracle WHERE us_id = :1"
    if id_check(userid, userpass) :
        cursor.execute(sql, [userid])
        conn.commit
    else :
        print('회원 정보를 잘못입력하셨습니다.')
    
# id체크
def id_check(userid, userpass):
    sql = "SELECT COUNT(*) FROM us_oracle WHERE us_id = :1 AND us_pw = :2"
    cursor.execute(sql, [userid, userpass])
    if cursor.fetchone()[0] == 1:
        return 1  # 회원승인
    sql = "SELECT COUNT(*) FROM us_oracle WHERE us_id = :1"
    cursor.execute(sql, [userid])
    if cursor.fetchone()[0] == 1:
        return 0  # 비밀번호 오류
    else:
        return -1  # 아이디가 존재하지 않음

# 관리자 계정인지 확인
def ad_check(userid, userpass):
    if userid == 'yj' and userpass == '1234' :
        return True
    else:
        return False

        
# 인사말
def hi(userid):
    sql = "SELECT us_name FROM us_oracle WHERE us_id = :1"
    cursor.execute(sql, [userid])
    result = cursor.fetchone()
    print(f'{result[0]}님 환영합니다!')
    return result[0]
    
# 회원정보조회
def listMember():
    cursor.execute("select * from us_oracle")
    rs = cursor.fetchall()
    if len(rs) == 0:
        print("등록된 회원정보가 존재하지 않습니다.")
    else:
        for row in rs:
            print(row)

# 특정회원정보조회
def us_view(userid):
    sql = "select * from us_oracle where us_id = :1"
    cursor.execute(sql, [userid])
    rs = cursor.fetchall()
    if len(rs) == 0:
        print("등록된 회원정보가 존재하지 않습니다.")
    else:
        for row in rs:
            print(row)


# 잔액 조회
def disp(userid):
    sql = "SELECT us_money FROM us_oracle WHERE us_id = :1"
    cursor.execute(sql, [userid])
    result = cursor.fetchone()
    print(f"{userid}님의 현재 페이머니 잔액은 {result[0]}원입니다.")
    
# 잔액 반환
def exist(userid):
    sql = "SELECT us_money FROM us_oracle WHERE us_id = :1"
    cursor.execute(sql, [userid])
    result = cursor.fetchone()
    return result[0]
    
# 결제
def outmoney(userid, price):
    sql = "UPDATE us_oracle SET us_money = us_money - :1 WHERE us_id = :2"
    cursor.execute(sql, [price, userid])
    print(f"{userid}님 {price}원만큼 결제 되었습니다.")

# 충전
def inmoney(userid, amount):
    sql = "UPDATE us_oracle SET us_money = us_money + :1 WHERE us_id = :2"
    cursor.execute(sql, [amount, userid])
    print(f"{userid}님의 페이머니가 {amount}원만큼 충전되었습니다.")
    disp(userid)
    
# 거래내역
def cr_insert(userid, itname, itprice, itvol):
    sql = "INSERT INTO cr_oracle(us_date, user_id, it_name, it_price, it_vol) VALUES (SYSDATE, :1, :2, :3, :4)"
    cursor.execute(sql, [userid, itname, itprice, itvol])
    conn.commit()
    
# 거래내역 조회
def cr_view(userid):
    sql = 'select * from cr_oracle where user_id = :1'
    cursor.execute(sql, [userid])
    rs = cursor.fetchall()
    
    if len(rs) == 0:
        print("등록된 거래정보가 존재하지 않습니다.")
    else:
        for row in rs:
            formatted_date = row[0].strftime('%Y-%m-%d %H:%M:%S')  # 날짜 형식 지정
            print((formatted_date,) + row[1:])

# 거래내역 전체 조회
def cr_viewall():
    cursor.execute('select * from cr_oracle')
    rs = cursor.fetchall()
    
    if len(rs) == 0:
        print("등록된 거래정보가 존재하지 않습니다.")
    else:
        for row in rs:
            formatted_date = row[0].strftime('%Y-%m-%d %H:%M:%S')  # 날짜 형식 지정
            print((formatted_date,) + row[1:])

# 문의사항 등록
def qs_insert(userid, quest):
    sql = "INSERT INTO qs_oracle VALUES (qs_seq.nextval, SYSDATE, :1, :2, '미확인')"
    cursor.execute(sql, [userid, quest])
    conn.commit()

# 문의사항 조회
def qs_view(userid):
    sql = 'select * from qs_oracle where user_id = :1'
    cursor.execute(sql, [userid])
    rs = cursor.fetchall()
    
    if len(rs) == 0:
        print("등록된 문의사항이 존재하지 않습니다.")
    else:
        for row in rs:
            date = row[1].strftime('%Y-%m-%d %H:%M:%S')  # 날짜 형식 지정
            print(f'문의 번호 : {row[0]}, 날짜 : {date}')
            print(f'회원 id : {row[2]}, 문의사항 : {row[3].read()}')
            print(f'관리자의 답변 : {row[4].read()}')
            print()
# 문의사항 전체 조회
def qs_viewall():
    cursor.execute('select * from qs_oracle')
    rs = cursor.fetchall()
    
    if len(rs) == 0:
        print("등록된 문의사항이 존재하지 않습니다.")
    else:
        for row in rs:
            date = row[1].strftime('%Y-%m-%d %H:%M:%S')  # 날짜 형식 지정
            print(f'문의 번호 : {row[0]}, 날짜 : {date}')
            print(f'회원 id : {row[2]}, 문의사항 : {row[3].read()}')
            print(f'관리자의 답변 : {row[4].read()}')
            print()
# 관리자 답변
def answer():
    qsno = input('문의번호를 입력하세요 : ')
    answer = input('답변을 입력하세요 : ')
    sql = 'update qs_oracle set answer = :1 where qs_no = :2'
    cursor.execute(sql,[answer,qsno])
    print('답변 등록이 완료되었습니다.')
    conn.commit
                   
# 거래 건수 불러오기
def trade_count(userid):
    sql = "SELECT COUNT(*) FROM cr_oracle WHERE user_id = :1"
    cursor.execute(sql, [userid])
    return cursor.fetchone()[0]

# 사용자의 vip상태
def vip_status(userid):
    count = trade_count(userid)
    vip_data = get_vip()
    
    current_grade = None
    next_trade_count = None
    
    for i, (grade, required_count, discount) in enumerate(vip_data):
        if count >= required_count:
            current_grade = grade
            if i < len(vip_data) - 1:
                next_trade_count = vip_data[i+1][1] - count
            else:
                next_trade_count = 0
    return current_grade, next_trade_count

# 텍스트 파일을 기본 텍스트 에디터로 열기
def edit_vip_info():
    import os
    os.system("notepad vip_info.txt")

# vip 정보 불러오기(리스트내포)
def get_vip():
    with open('vip_info.txt', 'r') as file:
        data = [line.strip().split(',') for line in file]
        vip_data = [(grade, int(required_count), int(discount)) for grade, required_count, discount in data]
    return vip_data

# vip 정보 업데이트
def vip_update():
    sql = "SELECT us_id FROM us_oracle"
    cursor.execute(sql)
    all_users = cursor.fetchall()
    for user in all_users:
        userid = user[0]
        current_grade, next_trade_count = vip_status(userid)
        sql = "UPDATE us_oracle SET vip = :1 WHERE us_id = :2"
        cursor.execute(sql, [current_grade, userid])
    conn.commit() 

# vip 결제
def vip_price(itprice, itvol, userid):
    price = itprice * itvol
    data = get_vip()
    grade, count = vip_status(userid)
    for a, _, discount in data:
        if a == grade :
            if discount == 0:
                return price
            else :
                return price * (100-discount)/100
            
        
        
        