#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[1]:


## 모듈 불러오기
from cx_Oracle import *
from menu import *
from user import *
from item import *
from basket import *
import cx_Oracle as cx

conn = cx.connect("scott", "1234", "localhost:1521/xe")
cursor = conn.cursor()
ch=0
us_ch = 0
ad_ch = 0
while ch != 3 :
    # 회원가입 or 로그인
    ch = menu()
    ## 로그인(chckId로 계정을 확인하는 경우 오라클 데이터베이스에 있는 데이터를 읽어와서 비교 후 판단)
    if ch == 1:
        ## id 입력
        userid, userpass = insertkey()
        ## 관리자 계정
        if ad_check(userid, userpass) :
            while ad_ch != 5:
                update()
                print()
                print('관리자계정으로 접속하셨습니다.')
                ### 관리자 메뉴 선택
                ad_ch = ad_menu()
                #### 회원 정보 조회
                if ad_ch == 1 :
                    ad_ch1 = ad_ch1_menu()
                    ##### 전체 회원 조회(거래내역은 특정 회원 정보 조회 시 보여줌)
                    if ad_ch1 == 1 :
                        listMember()
                    ##### 특정 회원 정보 조회(거래내역은 이때만 보여줌)
                    elif ad_ch1 == 2 :
                        userid = input('회원의 id를 입력하세요 : ')
                        us_view(userid)
                        cr_view(userid)
                        qs_view(userid)
                        ###### 특정 회원의 정보를 수정하시겠습니까?
                        change1 = change_menu()
                        if change1 == 1 :
                            print('회원 정보 수정을 진행합니다.')
                            print('어떻게 수정하시겠습니까?')
                            userpass, username = insertpn()
                            update(userid, userpass, username)
                        elif change1 == 2:
                            num = input('정말 회원탈퇴를 진행하시겠습니까? (y/n) : ')
                            if num == 'y' :
                                userpass = input('회원의 비밀번호를 입력하세요 : ')
                                delete(userid, userpass)
                                print('회원이 삭제되었습니다.')
                            else :
                                continue
                    elif ad_ch1 == 3:
                        cr_viewall()

                ##### 상품 목록 및 수정
                elif ad_ch == 2:
                    listItemall()
                    ##### 상품 목록을 수정
                    ch3 = int(input('상품 목록을 수정하시겠습니까?(추가:1)(변경:2)(삭제:3) :'))
                    if ch3 == 1 :
                        initem()
                    elif ch3 == 2:
                        ad_itupdate()
                    elif ch3 == 3:
                        ad_itdelete()
                    else :
                        print('잘못입력하셨습니다.')
                ##### 문의사항 조회
                elif ad_ch == 3:
                    qs_viewall()
                    num = input('답변을 하시겠습니까?(y/n) : ')
                    if num == 'y' :
                        answer()
                ##### vip 혜택 수정
                elif ad_ch == 4:
                    choice = int(input("1. VIP 정보 보기, 2. VIP 정보 수정 : "))
                    if choice == 1:
                        vip_data = get_vip()
                        for grade, required_count, discount in vip_data:
                            print(f"{grade}: {required_count} 거래 필요, {discount}% 할인")
                    elif choice == 2:
                        edit_vip_info()
                        print("수정 후 프로그램을 재시작해주세요.")
                    else :
                        print('잘못입력하셨습니다.')

                ##### 로그아웃
                elif ad_ch == 5:
                    print('로그아웃했습니다.')

                ##### 잘못입력
                else :
                    print('잘못입력하셨습니다.')
                    
        
        elif id_check(userid, userpass) == 1 :
            while us_ch != 7 :
                update()
                vip_update()
                print()
                current_grade, next_trade_count = vip_status(userid)
                if int(current_grade[3]) < 1:
                    event_menu()
                    print('vip1 이상은 광고문구가 뜨지 않습니다.')
                # 방문인사
                username=hi(userid)
                ### 사용자 메뉴 선택
                us_ch = us_menu()
                #### 회원 정보 조회(거래내역 포함) 및 수정
                if us_ch == 1 :
                    us_ch1 = us_ch1_menu()
                    ##### 거래내역 출력
                    if us_ch1 == 1 :
                        cr_view(userid)
                    #### 회원 정보 수정
                    elif us_ch1 == 2 :
                        print('회원 정보 수정을 진행합니다.')
                        print('어떻게 수정하시겠습니까?')
                        userpass, username = insertpn()
                        update(userid, userpass, username)

                #### 페이머니
                elif us_ch == 2 :
                    num = int(input('조회(1), 충전(2) : '))
                    if num == 1:
                        disp(userid)
                    elif num == 2:
                        amount = int(input('얼마를 충전하시겠습니까? : '))
                        inmoney(userid, amount)
                    else :
                        print('잘못입력했습니다.')
                #### 상품목록
                elif us_ch == 3 :
                    listItem()
                    itname = input('장바구니에 추가할 상품의 이름을 입력하세요. : ')
                    itvol = int(input('몇개를 담으시겠습니까? : '))
                    # bk 테이블 개수 조정
                    itprice = bk_price(itname)
                    try :
                        bk_insert(userid, itname, itprice, itvol)
                    except IntegrityError as e :
                        print('해당물품은 이미 장바구니에 있습니다. 장바구니를 확인하여 개수 조정을 부탁드립니다.')
                        continue
                    print(f'{itname}을 {itvol}개 담으셨습니다.')

                #### 장바구니 조회
                elif us_ch == 4 :
                    bk_view(userid)
                    num = int(input('수량 변경(1), 결제(2), 종료(3) : '))
                    if num == 1:
                        itname = input('바꾸실 상품명을 입력해주세요 : ')
                        bk_vol(userid, itname)
                    elif num == 2:
                        disp(userid)
                        itname = input('어떤 상품을 결제하시겠습니까? : ')
                        itvol = int(input('몇 개 결제하시겠습니까? : '))
                        itprice = bk_price(itname)
                        if invol(itname) - itvol >= 0:
                            price = vip_price(itprice, itvol, userid)
                            print(f'현재 회원님의 등급은 {current_grade}입니다.')
                            if exist(userid) - price >= 0:
                                # 지갑에서 돈 빼기
                                outmoney(userid, price)
                                # 장바구니에서 물건 빼기
                                bk_update(userid, itname, itvol)
                                # 상품목록에서 물건 빼기
                                itupdate(itname, itvol)
                                # 거래목록에 등록하기
                                cr_insert(userid, itname, itprice, itvol)
                            else :
                                print(f'잔액이 {abs(exist(userid) - price)}만큼 부족합니다.')
                        else :
                            print(f'재고가 {invol(itname) - itvol}개 부족합니다.')  
                    else :
                        continue
                #### vip 혜택
                elif us_ch ==5:
                    event_menu()
                    current_grade, next_trade_count = vip_status(userid)
                    print(f'현재 {username}님의 vip등급은 {current_grade}입니다.')
                    print(f'다음 등급까지 남은 거래 건수는 {next_trade_count}회입니다.')
                #### 문의사항
                elif us_ch == 6:
                    qs_view(userid)
                    num = input('문의사항을 등록하시겠습니까? (y/n)')
                    if num == 'y' :
                        quest = input('문의사항을 입력하세요 : ')
                        qs_insert(userid, quest)
                        print('등록이 완료되었습니다.')
                #### 로그아웃
                elif us_ch == 7:
                    print('로그아웃했습니다.')
                #### 회원탈퇴
                elif us_ch == 8 :
                    num = input('정말 회원탈퇴를 하시겠습니까? (y/n) : ')
                    if num == 'y' :
                        userpass, username = insertpn()
                        delete(userid, userpass)
                        us_ch = 7
                    else :
                        continue
                #### 잘못 입력 시
                else :
                    print('잘못입력하셨습니다.')
        #### 비밀번호틀림
        elif id_check(userid,userpass) == 0 :
            print('비밀번호가 틀렸습니다.')
        
        #### 로그인 실패
        else :
            print('등록된 회원이 존재하지 않습니다.')
        
    ## 회원가입
    elif ch == 2 :
        print('회원가입을 시작합니다.')
        userid, userpass, username = insertall()
        insert(userid, userpass, username)
        
    ## 프로그램 종료
    elif ch == 3 :
        print('프로그램이 종료되었습니다.')
        
    ## 잘못 입력 시
    else :
        print('잘못입력하셨습니다.')
conn.commit()
close()

