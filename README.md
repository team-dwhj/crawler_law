# crawler_law
## flask
### start_flask.py
해당 파일을 실행한 후에 브라우저에서 'localhost:5000'에 접속하면 flask 애플리케이션을 사용할 수 있습니다.
### /flask_app/__init__.py
1. start_flask.py에서 import하는 파일이며, flask 애플리케이션의 main함수와 같은 역할입니다.
2. @app.route('path')
사용자가 'localhost:5000/path'에 접속했을 때 바로 아래에 정의된 함수를 실행시킵니다.
3. render_template('file.html')
html문서를 렌더링합니다.
4. redirect('path')
해당 path를 지니는 url로 리디렉션합니다.
path에 상응하는 함수가 수행됩니다.
