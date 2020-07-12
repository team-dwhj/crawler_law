from flask import Flask, request, session, render_template, url_for, redirect
from requests import get
from os import path
from csv import reader


# configure app
app = Flask(__name__)
app.debug = True                                # 파일이 수정될 때마다 바로 빌드됨
app.secret_key = 'SuperSecret'                  # flask session 생성 위한 key


def get_list(list_name):
    script_dir = path.dirname(__file__)
    rel_path = "/form/" + list_name

    ret = []
    with open(script_dir + rel_path, newline='') as fp:
        ret = list(reader(fp))
    print(ret)
    return ret

@app.route("/", methods=['GET', 'POST'])
def search_case():
    print('index')
    print(session)

    if request.method == 'GET':
        # session configuration (flask의 session이며, requests의 session과는 별개)
        session.clear()                                 # session에 저장된 (key, value) pair 초기화
        session.permanent = True                        # session의 유효기간을 한달로

        # TODO-HJ 캡챠 가져오기

        # TODO-DW case_form.html에 캡챠 이미지 추가하기 
        return render_template('case_form.html', sch_bub_nm_list=get_list('sch_bub_nm'), sa_gubun_list=get_list('sa_gubun'))    # ./templates/case_form.html 렌더링

    elif request.method == 'POST':
        session.update(request.form)                # post request로 받아온 사건 정보를 session에 저장

        # TODO-DW 사건검색결과 parsing

        return redirect(url_for('gen_doc'))         # gen_doc()함수에 상응하는 주소로 redirect


@app.route("/gen_doc")
def gen_doc():
    print('gen_doc')
    print(session)

    if request.args is None:
        return redirect(get(request.host_url[:-1] + url_for('gen_doc'), {'gen_doc_begin':True}).url)

    else:
        # TODO-HJ 문서 생성 (경로는 ./static에)

        #while not path.isfile('/documents/doc.docx'):   # 파일이 생성될때까지 wait
        #    pass

        return redirect(url_for('down_doc'))        # down_doc()에 상응하는 주소로 redirect

@app.route("/down_doc")
def down_doc():
    print('down_doc')
    print(session)

    return render_template('down_doc.html')         # ./templates/down.doc.html 렌더링
