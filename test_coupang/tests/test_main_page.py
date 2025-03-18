# tests/test_main_page.py

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver # noqa
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pages.main_page import MainPage
from pages.login_page import LoginPage
from selenium.common.exceptions import NoSuchElementException , TimeoutException
#from pages.config import EMAIL,PASSWORD
from urllib import parse

class TestMainPage:
    def setup(self):
        self.driver = webdriver.Chrome()
    
    def teardown(self):
        self.driver.quit()

    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_open_main_page(self, driver: WebDriver):
    
        try:
            main_page = MainPage(driver)
            main_page.open()

        # 로그인 페이지(accounts)로 이동했는지 확인
            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

        except NoSuchElementException as e:
            assert False

    #자동로그인
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_login_test(self,driver:WebDriver):
        try:
            main_page = MainPage(driver)
            login_page = LoginPage(driver)
            main_page.open()
        
            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            time.sleep(2)

            main_page.click_LINK_TEXT("로그인")

            time.sleep(2)
            
            login_page.input_password_and_email()

            time.sleep(2)
            login_page.click_login_button()

            time.sleep(7)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url, "로그인 후 메인 페이지로 돌아오지 않았습니다."
            
            driver.save_screenshot("로그인 성공.jpg")

        except NoSuchElementException as e:
            driver.save_screenshot('로그인-실패-요소없음.jpg')  # 요소를 찾을 수 없을 때
            assert False, f"로그인 실패: 필수 요소를 찾을 수 없습니다. {e}"

        except TimeoutException as e:
            driver.save_screenshot('로그인-실패-시간초과.jpg')  # 시간 초과 발생
            assert False, f"로그인 실패: 페이지 로드가 시간이 초과되었습니다. {e}"

        except AssertionError as e:
            driver.save_screenshot('로그인-실패-검증오류.jpg')  # 검증 오류 발생
            assert False, f"로그인 실패: {e}"

        except Exception as e:
            driver.save_screenshot('로그인-실패-기타오류.jpg')  # 기타 예외 상황
            assert False, f"로그인 실패: 알 수 없는 오류 발생 - {e}"


    #노트북 검색 필터 (삼성전자 브랜드 선택과 가격 필터 결정)
    #@pytest.mark.skip(reason="테스트")
    def test_filter_search(self, driver:WebDriver):
        try:
            ITEMS_XPATH = "//img"  # 검색된 노트북 이미지
            main_page = MainPage(driver)
            main_page.open()

            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            main_page.search_items('노트북')

            wait.until(EC.presence_of_all_elements_located((By.XPATH, ITEMS_XPATH)))
            items = driver.find_elements(By.XPATH, ITEMS_XPATH)

            time.sleep(2)
            
            brand = ws(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='searchBrandFilter']/ul/li[1]/label")))
            driver.execute_script("arguments[0].scrollIntoView();", brand)


            time.sleep(2)
            actions = ActionChains(driver)
            actions.move_to_element(brand).click().perform()

            time.sleep(2)
            
            #가격 필터
            minprice = ws(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@title='minPrice']")))
            minprice.send_keys("300000")

            maxprice = ws(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@title='maxPrice']")))
            maxprice.send_keys("1000000")

            time.sleep(2)
            
            search_button = ws(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='searchPriceFilter']/div/a")))
            search_button.click()


        except TimeoutException as e:
        # Timeout 발생 시 처리
            driver.save_screenshot("검색-시간초과.jpg")
            assert False, f"Timeout 발생: {e}"

        except NoSuchElementException as e:
        # 요소를 찾지 못했을 때 처리
            driver.save_screenshot("검색-요소없음.jpg")
            assert False, f"요소를 찾을 수 없습니다: {e}"

        except AssertionError as e:
        # Assertion 실패 시 처리
            driver.save_screenshot("검색-검증실패.jpg")
            assert False, f"Assertion 실패: {e}"

        except Exception as e:
        # 기타 예외 상황 처리
            driver.save_screenshot("검색-기타오류.jpg")
            assert False, f"예기치 못한 오류 발생: {e}"
            
        
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_add_cart(self, driver:WebDriver):
        try:
            ITEMS_XPATH = "//img"  # 검색된 노트북 이미지
            CART_BUTTON_XPATH = "//button[contains(text(), '장바구니 담기')]"
            main_page = MainPage(driver)
            main_page.open()

            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            time.sleep(2)

            main_page.search_items('노트북')

            wait.until(EC.presence_of_all_elements_located((By.XPATH, ITEMS_XPATH)))
            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            
            time.sleep(2)

            if len(items) > 0:
                # 첫 번째 아이템 클릭 전 확인
                first_item = items[0]
                driver.execute_script("arguments[0].scrollIntoView();", first_item)  # 요소를 화면에 스크롤
                time.sleep(2)  # 요소 로드 대기
                first_item.click()  # 클릭
            else:
                assert False, "검색 결과가 비어 있습니다."

            time.sleep(2)

            wait.until(EC.presence_of_element_located((By.XPATH, CART_BUTTON_XPATH)))
            cart_button = driver.find_element(By.XPATH, CART_BUTTON_XPATH)
            cart_button.click()

            # 성공적으로 처리되었는지 확인
            time.sleep(2)

        # 스크린샷 저장
            driver.save_screenshot('장바구니-추가-성공.jpg')

        except NoSuchElementException:
            driver.save_screenshot('장바구니-추가-실패-요소없음.jpg')
            assert False, "요소를 찾을 수 없습니다."
        
        except TimeoutException:
            driver.save_screenshot('장바구니-추가-실패-시간초과.jpg')
            assert False, "요소 로드 시간이 초과되었습니다."

        except Exception as e:
            driver.save_screenshot('장바구니-추가-실패-기타오류.jpg')
            assert False, f"예기치 못한 오류: {e}"




    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_click_link_text(self, driver:WebDriver):
        try:
            main_page = MainPage(driver)
            main_page.open()

        # 로그인 페이지(accounts)로 이동했는지 확인
            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            main_page.click_LINK_TEXT("로그인")
            assert "login" in driver.current_url
            driver.save_screenshot('메인페이지-로그인-성공.jpg')

            time.sleep(2)
            driver.back()
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            time.sleep(2)
            main_page.click_LINK_TEXT('회원가입')
            assert "memberJoinFrm" in driver.current_url
            driver.save_screenshot('메인페이지-회원가입-성공.jpg')

            time.sleep(2)
            driver.back()
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            time.sleep(2)
            main_page.click_LINK_TEXT('장바구니')
            assert "cartView" in driver.current_url
            driver.save_screenshot('메인페이지-장바구니-성공.jpg')

            time.sleep(2)
            driver.back()
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            time.sleep(2)
            main_page.click_LINK_TEXT('마이쿠팡')
            assert "login" in driver.current_url
            driver.save_screenshot('메인페이지-마이쿠팡-성공.jpg')

        except NoSuchElementException as e:
            driver.save_screenshot('메인페이지-링크텍스트-실패-노서치.jpg')
            assert False
            
        except TimeoutError as e:
            driver.save_screenshot('메인페이지-링크텍스트-실패-타임에러.jpg')
            assert False

    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_search_items(self,driver:WebDriver):
        try:
            ITEMS_XPATH = "//form//ul/li"
            main_page = MainPage(driver)
            main_page.open()

        # 로그인 페이지(accounts)로 이동했는지 확인
            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증

            time.sleep(2)

            main_page.search_items('노트북')

            ws(driver,10).until(EC.presence_of_element_located((By.XPATH, ITEMS_XPATH)))
            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')

            assert len(items) > 0
            assert item_name in driver.current_url

            driver.save_screenshot('메인페이지-검색-성공.jpg')
            
        except NoSuchElementException as e:
            driver.save_screenshot('메인페이지-검색-실패-노서치.jpg')
            assert False
            
        except TimeoutError as e:
            driver.save_screenshot('메인페이지-검색-실패-타임에러.jpg')
            assert False
            