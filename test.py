import json
import os
import shutil
import tempfile
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def lambda_handler_local_test():
    try:
        # index.html 파일이 로컬에 있는지 확인
        key = 'index.html'
        local_dir = "C:/Projects/resume"
        local_html_path = os.path.join(local_dir, key)
        
        if not os.path.exists(local_html_path):
            print('index.html 파일이 없습니다. 종료합니다.')
            return {
                'statusCode': 400,
                'body': json.dumps('index.html 파일이 없습니다.')
            }

        # Chrome 옵션 설정
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 주석 처리하면 GUI 모드로 실행됩니다.
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--hide-scrollbars')

        # ChromeDriver 서비스 설정
        chrome_service = Service(executable_path='C:/Users/Jaeho/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')  # ChromeDriver의 경로를 지정하세요

        # 임시 디렉토리 생성
        with tempfile.TemporaryDirectory() as tmpdir:
            # index.html 파일 복사
            temp_html_path = os.path.join(tmpdir, 'index.html')
            shutil.copy(local_html_path, temp_html_path)
            
            # CSS 파일 복사
            css_file = 'styles.css'
            local_css_path = os.path.join(local_dir, css_file)
            if os.path.exists(local_css_path):
                shutil.copy(local_css_path, os.path.join(tmpdir, css_file))
            
            # 이미지 파일 복사
            img_profile = 'profile.jpg'
            local_img_path = os.path.join(local_dir, img_profile)
            if os.path.exists(local_img_path):
                shutil.copy(local_img_path, os.path.join(tmpdir, img_profile))

            # 이미지 파일 복사
            img_icon = 'icon.png'
            local_img_path = os.path.join(local_dir, img_icon)
            if os.path.exists(local_img_path):
                shutil.copy(local_img_path, os.path.join(tmpdir, img_icon))

            # HTML을 PDF로 변환
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            # 로컬 HTML 파일 로드
            driver.get(f'file://{temp_html_path}')
            
            # PDF 생성
            pdf_path = os.path.join(local_dir, 'resume.pdf')  # PDF 파일의 저장 위치
            pdf_options = {
                'printBackground': True,
                'paperWidth': 8.27,  # A4 width in inches
                'paperHeight': 11.69  # A4 height in inches
            }
            
            # PDF 저장
            pdf = driver.execute_cdp_cmd('Page.printToPDF', pdf_options)
            pdf_data = base64.b64decode(pdf['data'])  # base64로 인코딩된 데이터를 디코드
            
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)  # PDF 바이너리 데이터 저장
            
            driver.quit()

            print("PDF 파일이 생성되었습니다:", pdf_path)

        return {
            'statusCode': 200,
            'body': json.dumps('로컬 PDF 생성 완료')
        }

    except Exception as e:
        print(f'오류 발생: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'PDF 생성 오류: {str(e)}')
        }

# 로컬 테스트 실행
lambda_handler_local_test()
