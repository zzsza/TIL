from flask import Flask, request, url_for, redirect, render_template, session

app = Flask(__name__)


@app.route('/') # app.route 데코레이터로 위치를 말한다
def index():
    return 'index page'
    # return redirect(url_for('login')) 으로하면 재연결

@app.route('/user/<username>')
def show_post(username):
    return 'user %s' % username

@app.route('/login_form')
def login_form():
    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if ( request.form['username'] == 'jamie' and request.form['password'] == '1234'):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return request.form['username'] + " 님 환영합니다"
        else:
            return '로그인 정보가 맞지 않습니다'
    else:
        return '잘못된 접근'

# @app.route('/get_test', methods = ['GET']) # 실제 서비스에선 절대 get방식으로 로그인을 하지 않아요!! post로 해야함
# def get_test():
#     if request.method == 'GET':
#         if (request.args.get('username') == 'jamie' and request.args.get('password') == '1234'):
#             # http://127.0.0.1:5000/get_test?username=jamie&password=1234 로 접속하면 jamie님 환영합니다라고 나
#             return request.args.get('username') + " 님 환영합니다"
#         else:
#             return '로그인 정보가 맞지 않습니다'
#     else:
#         return '잘못된 접근'


@app.route('/template')
@app.route('/template/<tempid>')
def template_test(tempid=None):
    sports = ['야구', '축구', '농구']
    return render_template('template.html', tempid=tempid, sports=sports)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'sample_secret_key'


if __name__ == '__main__':
    app.run(debug=True)

