## 메뉴
def menu():
    print('방문을 환영합니다.')
    print('로그인(1), 회원가입(2), 프로그램 종료(3) :')
    num = int(input('번호를 입력하세요 :'))
    return num
def ad_menu():
    print('회원 정보 조회(1), 상품 목록 및 수정(2)')
    print('문의사항 조회(3), vip 혜택 수정(4), 로그아웃(5)')
    num = int(input('번호를 입력하세요 :'))
    return num

def ad_ch1_menu():
    print('전체 회원 조회(1), 특정회원 정보 조회(거래내역)(2), 전체 거래내역 조회(3)')
    num = int(input('번호를 입력하세요 :'))
    return num

def change_menu():
    num = int(input('해당 회원의 정보를 수정(1), 삭제(2) : '))
    return num

def us_menu():
    print('회원 정보 조회 및 수정(1), 페이머니(2)')
    print('상품 목록 조회(3), 장바구니(4), vip 혜택(5)')
    print('문의사항(6), 로그아웃(7), 회원탈퇴(8)')
    num = int(input('번호를 입력하세요 :'))
    return num

def us_ch1_menu():
    print('거래내역 출력(1), 회원 정보 수정(2)')
    num = int(input('번호를 입력하세요 :'))
    return num


    
def event_menu():
    print('================== 맴버십 혜택! =================')
    
    with open('vip_info.txt', 'r') as f:
        for line in f:
            grade, count, discount = line.strip().split(',')
            print(f'{grade} : 거래 내역이 {count}건 이상 => 전품목 {discount}%할인 !!')
    
    print('===============================================')