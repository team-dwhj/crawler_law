from flask import Flask, request, session, render_template, url_for, redirect
from requests import get
from os import path


# configure app
app = Flask(__name__)
app.debug = True                                # 파일이 수정될 때마다 바로 빌드됨
app.secret_key = 'SuperSecret'                  # flask session 생성 위한 key


@app.route("/", methods=['GET', 'POST'])
def index():
    print('index')
    print(session)

    if request.method == 'GET':
        # session configuration (flask의 session이며, requests의 session과는 별개)
        session.clear()                                 # session에 저장된 (key, value) pair 초기화
        session.permanent = True                        # session의 유효기간을 한달로

        # TODO 캡챠 가져오기
    
        return render_template('case_form.html')    # ./templates/case_form.html 렌더링

    elif request.method == 'POST':
        session.update(request.form)               # post request로 받아온 사건 정보를 session에 저장
        return redirect(url_for('gen_doc'))         # gen_doc()함수에 상응하는 주소로 redirect


@app.route("/gen_doc")
def gen_doc():
    print('gen_doc')
    print(session)

    if request.args is None:
        return redirect(get(request.host_url[:-1] + url_for('gen_doc'), {'gen_doc_begin':True}).url)

    else:
        # TODO 문서 생성 (경로는 ./documents에)

        #while not path.isfile('/documents/doc.docx'):   # 파일이 생성될때까지 wait
        #    pass

        return redirect(url_for('down_doc'))        # down_doc()에 상응하는 주소로 redirect

@app.route("/down_doc")
def down_doc():
    print('down_doc')
    print(session)

    return render_template('down_doc.html')         # ./templates/down.doc.html 렌더링
