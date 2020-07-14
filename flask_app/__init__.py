from flask import Flask, request, session, render_template, url_for, redirect
from requests import get
from os import path
from csv import reader
import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup

# configure app
app = Flask(__name__)
app.debug = True  # 파일이 수정될 때마다 바로 빌드됨
app.secret_key = 'SuperSecret'  # flask session 생성 위한 key


def get_list(list_name):
    script_dir = path.dirname(__file__)
    rel_path = "/form/" + list_name

    ret = []
    with open(script_dir + rel_path, newline='') as fp:
        ret = list(reader(fp))
    print(ret)
    return ret


def download_captcha_img():
    # Todo-HJ: url constant로 빼야함
    with requests.session() as s:
        http_response = s.get("https://safind.scourt.go.kr/sf/captchaImg?t=image")

        if http_response.status_code == 200:
            session['cookies'] = http_response.cookies.get_dict()

            # Todo-HJ: url 전략 필요
            basedir = path.abspath(path.dirname(__file__))
            image_dir = path.join(basedir, 'static', 'captcha.png')

            with open(image_dir, 'wb') as f:
                for chunk in http_response:
                    f.write(chunk)
            return True
        else:
            return False


def search_sagun(form_data):
    with requests.session() as s:
        # download_captcha_img 할 때 쿠키를 다시 가져옵니다.
        cookies = requests.cookies.merge_cookies(RequestsCookieJar(), session['cookies'])
        s.cookies = cookies

        url = 'https://safind.scourt.go.kr/sf/servlet/SFSuperSvl'
        # response: requests.models.Response = session.post(url, data=form_data, cookies=session.cookies)

        response: requests.models.Response = s.post(url, data=form_data)

        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            pass
        else:
            # Todo: Failure 처리
            pass

        # Todo: 전처리 코드

        # return bs
        #return BeautifulSoup
        print(response)
        return response.txt


@app.route("/", methods=['GET', 'POST'])
def search_case():
    print('index')
    print(session)

    if request.method == 'GET':
        # session configuration (flask의 session이며, requests의 session과는 별개)
        session.clear()  # session에 저장된 (key, value) pair 초기화
        session.permanent = True  # session의 유효기간을 한달로

        # TODO-HJ 캡챠 가져오기

        if download_captcha_img():
            # TODO-DW: 성공했을 때
            pass
        else:
            # Todo-DW: 실패했을 때
            pass

        # TODO-DW case_form.html에 캡챠 이미지 추가하기 
        return render_template('case_form.html',
                               force_refresh=session['cookies']['JSESSIONID'],
                               sch_bub_nm_list=get_list('sch_bub_nm'),
                               sa_gubun_list=get_list('sa_gubun'))  # ./templates/case_form.html 렌더링

    elif request.method == 'POST':
        session['form_data'] = request.form  # post request로 받아온 사건 정보를 session에 저장

        return redirect(url_for('gen_doc'))  # gen_doc()함수에 상응하는 주소로 redirect


@app.route("/gen_doc")
def gen_doc():
    print('gen_doc')
    print(session)

    if request.args is None:
        return redirect(get(request.host_url[:-1] + url_for('gen_doc'), {'gen_doc_begin': True}).url)

    else:
        # TODO-DW 사건검색결과 parsing
        return search_sagun(session['form_data'])
        
        # TODO-HJ 문서 생성 (경로는 ./static에)

        # while not path.isfile('/documents/doc.docx'):   # 파일이 생성될때까지 wait
        #    pass

        return redirect(url_for('down_doc'))  # down_doc()에 상응하는 주소로 redirect


@app.route("/down_doc")
def down_doc():
    print('down_doc')
    print(session)

    return render_template('down_doc.html')  # ./templates/down.doc.html 렌더링
