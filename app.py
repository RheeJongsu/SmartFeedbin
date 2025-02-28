# app.py
import streamlit as st
import datetime
import time
from dateutil.relativedelta import relativedelta
from modules import step1_user_setup, step2_install_dependencies
from modules import step3_func
from modules import step4_data
from modules import userParam as param

st.set_page_config(page_title="SmartFeedBin", page_icon="🔔", layout="wide")
# Layout
empty1, Contents1, empty2 = st.columns([0.1,1,0.1])
article1, article2, article3= st.columns(3)
 

def login():
    with st.spinner("Check up user..."):
        pass #step1_user_setup.create_user(username=username, password=password)
    try:
        st.session_state.ConnDB = step3_func.MYSQL_Connect()
    except Exception as e:  #Login Failed
        print(f"An error occurred during user setup: {e}")
        st.session_state.ConnDB = None
        st.session_state.MessageShow = f"<span style='color:red'> {e}</span>"

    # Download DB
    if st.session_state.ConnDB is None :
        st.error("Database connection failed. Please check your credentials.")
        st.session_state.MessageShow = f"<span style='color:red'> Database connection failed. Please check your credentials. </span>"
    else:    
        st.session_state.isLogin = True
        st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
        st.success("Loading Feedbin Data......")
        st.session_state.MessageShow = None
 
def main():
    ## Grobal Variable
    if 'isLogin' not in st.session_state :
        st.session_state.isLogin = False
    if 'MessageShow' not in st.session_state :
        st.session_state.MessageShow = None
    if 'ConnDB' not in st.session_state:
        st.session_state.ConnDB = None
    if 'userName' not in st.session_state:
        st.session_state.userName = None
    if 'mysqlDepthDataAll' not in st.session_state:
        st.session_state.mysqlDepthDataAll = None
    if 'mysqlFeedBinDataAll' not in st.session_state:
        st.session_state.mysqlFeedBinDataAll = None
    if 'dataIndex' not in st.session_state:
        st.session_state.dataIndex = 0
    if 'dataRaw' not in st.session_state:
        st.session_state.dataRaw = None
    if 'dataFiltered' not in st.session_state:
        st.session_state.dataFiltered = None
    if 'dataBound' not in st.session_state:
        st.session_state.dataBound = None
    if 'dataFeedBin' not in st.session_state:
        st.session_state.dataFeedBin = None        
    if 'Option' not in st.session_state:
        st.session_state.Option = None
    if 'IsLoad' not in st.session_state:
        st.session_state.IsLoad = False

    st.session_state.Debug = True

    ## Event Callback
    def updateSearchingDate(feedcheer):
        if(len(st.session_state.searchingDate) == 2):
            date_start = st.session_state.searchingDate[0]
            date_end = st.session_state.searchingDate[1]
            st.session_state.mysqlDepthDataAll = step3_func.MysqlGetFeedbinData(st.session_state.ConnDB, str(date_start), str(date_end), feedcheer)
    
    ## Side Bar
    st.sidebar.title("CONSTANTEC FEED CHECK \n 3D LiDAR 측정 시스템")
    st.sidebar.text(" ") 
    st.sidebar.text(" ") 


    if(st.session_state.isLogin):
        st.sidebar.text("{}님 안녕하세요.".format(st.session_state.userName))  
        if st.sidebar.button("Logout"):
            st.session_state.isLogin = False
            st.session_state.userName = None
            if(st.session_state.ConnDB is not None):
                st.session_state.ConnDB.close()
            st.session_state.IsLoad = False
            st.rerun()
             
        
        choice = st.sidebar.radio(" ", ["측정 데이터","측정 데이터(Raw)", "기타"])
        
        st.sidebar.text(" ") 
        st.sidebar.text(" ") 
        
        if st.sidebar.button("조회"):
            st.session_state.ConnDB = step3_func.MYSQL_Connect()
            st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
            st.cache_data.clear()
            st.cache_resource.clear()

    else:
        choice = st.sidebar.radio(" ", ["Login"])
    
    ## Main Contents
    with empty1:
        st.empty()
    with Contents1:
        ## Error Message
        if(st.session_state.MessageShow is not None):
            st.markdown(st.session_state.MessageShow, unsafe_allow_html=True)
        
        ## Login First Page
        if choice == "Login":
            #st.subheader("Mobile Login")
            st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:28px; font-weight:bold;'>Smart Feedbin App Login</p>", unsafe_allow_html=True)
            username = st.text_input("Username", value="Constantec")
            password = st.text_input("Password", value="root", type="password")
            st.session_state.userName = username
            if st.button("Login",on_click=login):
                st.rerun()

        ## 최근 정보를 열람
        elif choice == "측정 데이터":
             
            if "selected_tab" not in st.session_state:
                st.session_state.selected_tab = "피드빈1"
             
            options = ["피드빈1", "피드빈2", "피드빈3"]    
            
            #st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:18px; font-weight:bold; margin: 1px 0 0px 0; padding: 5px; border-radius: 5px;'>✅ 피드빈 선택</p>", unsafe_allow_html=True)   
            selected_option = st.radio("", options, index=options.index(st.session_state.selected_tab), horizontal=True)
            
            if st.session_state.selected_tab != selected_option:
                st.session_state.selected_tab = selected_option  # 변경된 탭 저장
                st.session_state.IsLoad = False  # 데이터 새로 로드 트리거
                                
            today = datetime.datetime.now()
            date_end = today
            date_start = today - datetime.timedelta(days=10)
            feedbin_seq = "0"
             
            if selected_option == "피드빈1":
                feedbin_seq = "13"
                col1, col2 = st.columns([1, 4])  # 첫 번째 컬럼(이미지) 작게, 두 번째 컬럼(텍스트) 크게 설정
                
                with col2:
                    date_start = today - datetime.timedelta(days=50)
                    print("bin1..... date_start new : ", date_start) 
                    st.session_state.selectLastData = step3_func.MysqlGetLastFeedbinData(st.session_state.ConnDB, str(date_start), str(date_end), feedbin_seq) 
                    
                    # 데이터 확인 후 처리
                    if not st.session_state.selectLastData.empty:
                        last_data = st.session_state.selectLastData.iloc[0]  # 첫 번째 결과 가져오기
                        stock_ratio = float(last_data["stock_ratio"])  # stock_ratio를 float으로 변환 (문자열 방지)

                        # stock_ratio 값에 따라 이미지 선택
                        if stock_ratio == 100:
                            image_path = "image/silo_100.png"
                        elif stock_ratio >= 90:
                            image_path = "image/silo_90.png"
                        elif stock_ratio >= 80:
                            image_path = "image/silo_80.png"
                        elif stock_ratio >= 70:
                            image_path = "image/silo_70.png"
                        elif stock_ratio >= 60:
                            image_path = "image/silo_60.png"
                        elif stock_ratio >= 50:
                            image_path = "image/silo_50.png"
                        elif stock_ratio >= 40:
                            image_path = "image/silo_40.png"
                        elif stock_ratio >= 30:
                            image_path = "image/silo_30.png"
                        elif stock_ratio >= 20:
                            image_path = "image/silo_20.png"
                        elif stock_ratio >= 10:
                            image_path = "image/silo_10.png"                            
                        else:
                            image_path = "image/silo_0.png"  #  기본 이미지 설정

                        st.markdown(
                            '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 농장명 : &nbsp &nbsp ' + last_data["farm_nm"] + '</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 측정일시 : &nbsp &nbsp ' + str(last_data["fistdt"]) + '&nbsp &nbsp ' +  str(last_data["lastdt"]) + '</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 재고율 : &nbsp &nbsp ' + str(round(last_data["stock_ratio"])) + '%</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 재고량 : &nbsp &nbsp ' + str(last_data["stock_amt"]) + '</p>',
                            unsafe_allow_html=True
                        )
                        
                    else:
                        st.write("📌 데이터가 없습니다.")
                        image_path = "image/silo_0.png"  # 데이터가 없을 경우 기본 이미지 설정    
                    
                with col1:
                    st.image(image_path, width=60)
                 
                
            elif selected_option == "피드빈2": 
                feedbin_seq = "14"
                col1, col2 = st.columns([1, 4])  # 첫 번째 컬럼(이미지) 작게, 두 번째 컬럼(텍스트) 크게 설정
                 
                with col2:
                    date_start = today - datetime.timedelta(days=50) 
                    print("bin2..... date_start new : ", date_start) 
                    st.session_state.selectLastData = step3_func.MysqlGetLastFeedbinData(st.session_state.ConnDB, str(date_start), str(date_end), feedbin_seq) 
                      
                    # 데이터 확인 후 처리
                    if not st.session_state.selectLastData.empty:
                        last_data = st.session_state.selectLastData.iloc[0]  # 첫 번째 결과 가져오기
                        stock_ratio = float(last_data["stock_ratio"])  # stock_ratio를 float으로 변환 (문자열 방지)

                        # stock_ratio 값에 따라 이미지 선택
                        if stock_ratio == 100:
                            image_path = "image/silo_100.png"
                        elif stock_ratio >= 90:
                            image_path = "image/silo_90.png"
                        elif stock_ratio >= 80:
                            image_path = "image/silo_80.png"
                        elif stock_ratio >= 70:
                            image_path = "image/silo_70.png"
                        elif stock_ratio >= 60:
                            image_path = "image/silo_60.png"
                        elif stock_ratio >= 50:
                            image_path = "image/silo_50.png"
                        elif stock_ratio >= 40:
                            image_path = "image/silo_40.png"
                        elif stock_ratio >= 30:
                            image_path = "image/silo_30.png"
                        elif stock_ratio >= 20:
                            image_path = "image/silo_20.png"
                        elif stock_ratio >= 10:
                            image_path = "image/silo_10.png"                            
                        else:
                            image_path = "image/silo_0.png"  #  기본 이미지 설정
 
                        st.markdown(
                            '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 농장명 : &nbsp &nbsp ' + last_data["farm_nm"] + '</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 측정일시 : &nbsp &nbsp ' + str(last_data["fistdt"]) + '&nbsp &nbsp ' +  str(last_data["lastdt"]) + '</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 사료 재고율 (%) : &nbsp &nbsp ' + str(last_data["stock_ratio"]) + '%</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 재고량 (Kg) : &nbsp &nbsp ' + str(last_data["stock_amt"]) + '</p> ',
                            unsafe_allow_html=True
                        )
                    else:
                        st.write("📌 데이터가 없습니다.")
                        image_path = "image/silo_0.png"  # 데이터가 없을 경우 기본 이미지 설정    
                        
                with col1:
                    st.image(image_path, width=60)
                        
            elif selected_option == "피드빈3": 
                feedbin_seq = "11" 
                col1, col2 = st.columns([1, 4])  # 첫 번째 컬럼(이미지) 작게, 두 번째 컬럼(텍스트) 크게 설정
                
                with col2:
                    date_start = today - datetime.timedelta(days=150) 
                    print("bin3..... date_start new : ", date_start) 
                    st.session_state.selectLastData = step3_func.MysqlGetLastFeedbinData(st.session_state.ConnDB, str(date_start), str(date_end), feedbin_seq) 
                     
                    # 데이터 확인 후 처리
                    if not st.session_state.selectLastData.empty:
                        last_data = st.session_state.selectLastData.iloc[0]  # 첫 번째 결과 가져오기
                        stock_ratio = float(last_data["stock_ratio"])  # stock_ratio를 float으로 변환 (문자열 방지)

                        #  stock_ratio 값에 따라 이미지 선택
                        if stock_ratio == 100:
                            image_path = "image/silo_100.png"
                        elif stock_ratio >= 90:
                            image_path = "image/silo_90.png"
                        elif stock_ratio >= 80:
                            image_path = "image/silo_80.png"
                        elif stock_ratio >= 70:
                            image_path = "image/silo_70.png"
                        elif stock_ratio >= 60:
                            image_path = "image/silo_60.png"
                        elif stock_ratio >= 50:
                            image_path = "image/silo_50.png"
                        elif stock_ratio >= 40:
                            image_path = "image/silo_40.png"
                        elif stock_ratio >= 30:
                            image_path = "image/silo_30.png"
                        elif stock_ratio >= 20:
                            image_path = "image/silo_20.png"
                        elif stock_ratio >= 10:
                            image_path = "image/silo_10.png"                            
                        else:
                            image_path = "image/silo_0.png"  # 기본 이미지 설정
  
                        st.markdown(
                            '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 농장명 : &nbsp &nbsp ' + last_data["farm_nm"] + '</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 측정일시 : &nbsp &nbsp ' + str(last_data["fistdt"]) + '&nbsp &nbsp ' +  str(last_data["lastdt"]) + '</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 사료 재고율 (%) : &nbsp &nbsp ' + str(last_data["stock_ratio"]) + '%</p> '
                            + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #0A0A30, #10104A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">&nbsp 재고량 (Kg) : &nbsp &nbsp ' + str(last_data["stock_amt"]) + '</p> ',
                            unsafe_allow_html=True
                        )
                    else:
                        st.write("📌 데이터가 없습니다.")
                        image_path = "image/silo_0.png"  # 데이터가 없을 경우 기본 이미지 설정    
                                                    
                with col1:
                    st.image(image_path, width=60)
                        
            row1 = st.columns(1)  # 첫 번째 행
            row2 = st.columns(1)  # 두 번째 행
 
            # 30days Infomation
            #if(st.session_state.IsLoad == False):   
            if not st.session_state.IsLoad:    
                
                st.session_state.mysqlDepthDataAll = step3_func.MysqlGetFeedbinData(st.session_state.ConnDB, str(date_start), str(date_end), feedbin_seq) 
                st.session_state.IsLoad = True
                print("[DataLoad] Complete : ", date_start, feedbin_seq) 
                st.rerun()
            
                        
            # with article1:
            with row1[0]:
                #st.markdown("📊 피드빈 측정 리스트")                
                st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:18px; font-weight:bold; margin: 3px 0;'>📊 피드빈 측정 리스트</p>", unsafe_allow_html=True)
                 
                # Data Table
                event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['fistdt','lastdt','stock_ratio','stock_amt','desc']],
                        column_config={
                            "fistdt": st.column_config.Column(
                                label="측정일자",                            
                            ),
                            "lastdt": st.column_config.Column(
                                label="시간",
                            ),
                            "stock_ratio": st.column_config.NumberColumn(
                                label="재고율",  
                                format="%.0f%%"  # 백분율(%) 변환 
                            ),
                            "stock_amt": st.column_config.Column(
                                label="재고량",
                            ),
                            "desc": st.column_config.Column(
                                label="비고",
                                width=200
                            )},
                        use_container_width=True,  # 전체 너비 확장
                        height=250,  # 표의 높이 조절 (픽셀 단위)
                        on_select='rerun',
                        selection_mode='single-row'
                        )
                
                # HTML/CSS 스타일이 적용된 구분선 추가
                st.markdown("<hr style='border:1px solid #a26; margin:1px 0; padding: 0;'> <br>", unsafe_allow_html=True)
  
                # Select Data                
                if len(event.selection['rows']):
                    st.session_state.dataIndex = int(event.selection['rows'][0])
                    dataRaw = step3_func.SelectDataFromMYSQL(st.session_state.mysqlDepthDataAll, st.session_state.dataIndex)  # 거리 데이터 추출
                    # 사료통 크기 정보를 이용한 선택(동일 용량이 있는 경우 변경해야함) 
                    dataSize = step3_func.SelectSizeFeedBinFromSQL(st.session_state.mysqlFeedBinDataAll, st.session_state.mysqlDepthDataAll.std_volume[st.session_state.dataIndex])
                    
                    st.session_state.dataRaw = dataRaw
                    st.session_state.dataFeedBin = dataSize
                    
                    # 체크된 행의 정보를 한줄로 보여줌.
                    selected_index = int(event.selection['rows'][0])
                    selected_row = st.session_state.mysqlDepthDataAll.loc[selected_index]
                      
  
            #with article2:
            with row2[0]:
                  
                if(st.session_state.dataRaw is not None):   
                    #st.markdown("📌 측정 데이터")                
                    st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:18px; font-weight:bold; margin: 1px 0;'>⏳ 측정 데이터</p>", unsafe_allow_html=True)
                    step4_data.Show3DFeedBin(st.session_state.dataRaw, st.session_state.dataFeedBin)
                    st.session_state.dataRaw = None
                else:
                    st.write(" ")  # 데이터가 없을 경우 메시지 표시 (필요하면 제거 가능)
                    
                    
 
        # 사료통 없는 사료 정보를 확대해서 보여주는 요소
        elif choice == "측정 데이터(Raw)":
            
            st.session_state.mysqlDepthDataAll = None  # 기본값 
            st.session_state.selectLastData = None  # 기본값
                        
            st.session_state.selected_tab = "피드빈1"
             
            options = ["피드빈1", "피드빈2", "피드빈3"]    
            #st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:18px; font-weight:bold; margin: 1px 0 0px 0; padding: 5px; border-radius: 5px;'>✅ 피드빈 선택</p>", unsafe_allow_html=True)   
            selected_option = st.radio("", options, index=options.index(st.session_state.selected_tab), horizontal=True)
            
            if st.session_state.selected_tab != selected_option:
                st.session_state.selected_tab = selected_option  # 변경된 탭 저장
                st.session_state.IsLoad = False  # 데이터 새로 로드 트리거
                
            today = datetime.datetime.now()
            date_end = today
            date_start = today - datetime.timedelta(days=10)
            feedbin_seq = "0"    
            
            if selected_option == "피드빈1":
                feedbin_seq = "13"
            elif selected_option == "피드빈2":
                feedbin_seq = "14"
            elif selected_option == "피드빈3":
                feedbin_seq = "11"
                        
            print("처리내역  1   -------------- ", feedbin_seq)
                        
            row1 = st.columns(1)  # 첫 번째 행
            row2 = st.columns(1)  # 두 번째 행
    
            # 상단 row
            with row1[0]: 
                #st.markdown("📊 피드빈 측정 리스트")                
                st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:18px; font-weight:bold; margin: 3px 0;'>📊 피드빈 측정 리스트</p>", unsafe_allow_html=True)
                 
                ## Title
                # st.title("CONSTANTEC FEED CHECK \n 3D LiDAR 측정 시스템 (3D Bin Manager 1.0)") 
                # st.markdown("*측정 데이터 조회 선택")
                # 검색일 선택 (위와 동일한 형태로 중복성 방지 필요)
                today = datetime.datetime.now()
                month_ago_2 = today - relativedelta(months=10)
                 
                print("처리내역  2   -------------- ", feedbin_seq)
            
            
                if "searchingDate" not in st.session_state:
                    st.session_state.searchingDate = (month_ago_2, today)
    
                d = st.date_input(" ** 측정일을 선택하세요.",
                                (month_ago_2,today),
                                max_value=today,
                                format="YYYY-MM-DD",
                                key='searchingDate',
                                on_change=updateSearchingDate(feedbin_seq))
                
                # Data Table (위와 동일한 형태로 중복성 방지 필요)
                event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['fistdt','lastdt','stock_ratio','stock_amt','desc']],
                        column_config={
                            "fistdt": st.column_config.Column(
                                label="측정일자",                            
                            ),
                            "lastdt": st.column_config.Column(
                                label="시간",
                            ),
                            "stock_ratio": st.column_config.NumberColumn(
                                label="재고율",  
                                format="%.0f%%"  # 백분율(%) 변환 
                            ),
                            "stock_amt": st.column_config.Column(
                                label="재고량",
                            ),
                            "desc": st.column_config.Column(
                                label="비고",
                                width=200 
                            )},
                        use_container_width=True,  # 전체 너비 확장
                        height=250,  # 표의 높이 조절 (픽셀 단위)     
                        on_select='rerun',
                        selection_mode='single-row'
                        )
            
                # HTML/CSS 스타일이 적용된 구분선 추가
                st.markdown("<hr style='border:1px solid #a26; margin:1px 0; padding: 0;'> <br>", unsafe_allow_html=True)
   
                # 선택한 행의 정보를 추출
                selected_index = None  # 초기화 추가
                # Select Data (유사하나 출력 방식이 다름)                 
                if len(event.selection['rows']):
                    st.session_state.dataIndex = int(event.selection['rows'][0])
                    dataRaw = step3_func.SelectDataFromMYSQL(st.session_state.mysqlDepthDataAll, st.session_state.dataIndex)  # 거리 데이터 추출 
                    st.session_state.dataRaw = dataRaw
                    
            # 하단 row
            with row2[0]:
                if st.session_state.dataRaw is not None: 
                    #st.markdown("📌 측정 데이터")                
                    st.markdown("<p style='color:rgb(156, 223, 231); background:rgb(19, 49, 59); font-size:18px; font-weight:bold; margin: 1px 0;'>⏳ 측정 데이터</p>", unsafe_allow_html=True)                   
                    dataRaw = st.session_state.dataRaw
                    step4_data.Show3DRawData(dataRaw)
                    #print("Select Row", st.session_state.dataIndex)
        
        
        
        # 프로그램 Option 변경으로 Python의 변수를 활용함 (정리 혹은 변경 필요)
        elif choice == "기타":
            st.subheader("데이터 화면 옵션") 

            # Layout
            col1, col2 , col3= st.columns(3)

            optionFeedbinMode = ['모두', '절반', '벽 없음']
            with col1:
                st.markdown("Mesh")
                st.slider("사료 투명도",0,100,value=param.DISPLAY_MESH_ALPHA,key="newMeshAlpha" , on_change=param.ChageMeshAlpha)
                DISPLAY_MESH_COLORMAP = st.selectbox("Color Map",param.DISPLAY_COLORMAP_LIST,index=39) 
            with col2:
                st.markdown("Grid")
                DISPLAY_GRID_ALPHA = st.slider("선 투명도",0,100,value=param.DISPLAY_GRID_ALPHA)
                DISPLAY_GRID_COLOR = st.color_picker("Grid Color",param.DISPLAY_GRID_COLOR)
            with col3:
                st.markdown("Feedbin")
                DISPLAY_TOPWALL_ALPHA = st.slider("통 투명도",0,100,value=param.DISPLAY_WALL_ALPHA)
                DISPLAY_TOPWALL_COLOR = st.color_picker("통 상단 Color",param.DISPLAY_WALL_COLOR)
                DISPLAY_TOPWALL_DENSITY = st.slider("통 밀도",10,100,value=param.DISPLAY_TOPWALL_DENSITY)
                DISPLAY_BOTTOMWALL_COLOR = st.color_picker("통 하단 Color",param.DISPLAY_BOTTOMWALL_COLOR)
                DISPLAY_BOTTOMWALL_DENSITY = st.slider("사료 밀도",10,100,value=param.DISPLAY_BOTTOMWALL_DENSITY)
                selectionWallMode = st.selectbox(
                    "사료통 출력 모드",
                    optionFeedbinMode,
                    index=param.DISPLAY_TOPWALL_MODE,
                )
                DISPLAY_TOPWALL_MODE = optionFeedbinMode.index(selectionWallMode)
            
            st.markdown("3D LiDAR PointCloud")
            DISPLAY_SCATTER_POINT_SIZE = st.slider("점 크기",3,20,value=param.DISPLAY_SCATTER_POINT_SIZE)

            if(st.button("reset")):
                param.Initialize()
                st.rerun()
    with empty2:
        st.empty()

    #Debug용
    #print("Done", step3_func.DISPLAY_MESH_COLORMAP)

if __name__ == "__main__":
    main()
