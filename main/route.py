from flask import Blueprint, request, render_template, make_response, session, redirect, url_for
from .User.sing_up import get_users, sing_up, Model, pw_check, update_items, delete_token
from markupsafe import escape
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

main = Blueprint("route", __name__)


@main.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user_name=escape(session['user_id']))
    else:
        return "회원가입 및 로그인을 해주세요! <br><a href = '/login'> 로그인 하러가기! </a><br><a href = '/register'> 회원가입 하러가기! "


@main.route('/register', methods=['POST', 'GET'])
def registry():
    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        password = request.form['password']

        if len(get_users(user_id)['Items']) == 0:
            user_info = Model(user_id=user_id, name=name, password=password)
            sing_up(user_info.user_model())
            return f'''
                    <script>
                        alert('{name}님이 성공적으로 등록되었습니다!')
                        location.href = '/'
                    </script>
                '''
        else:
            return f'''
                    <script>
                        alert('{name}님은 이미 등록되어있습니다.')
                        location.href = '/register'
                    </script>
                '''
    else:
        return render_template('register.html')


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['password']

        if len(get_users(user_id)['Items']) != 0:
            password = get_users(user_id)['Items'][0]['password']
            if pw_check(user_pw, password):
                access_token = create_access_token(identity=user_id)
                resp = make_response(redirect('/'))
                resp.set_cookie('user_access_token', access_token)
                update_items(user_id, access_token)
                session['user_id'] = user_id
                return resp
            else:
                return f'''
                    <script>
                        alert('아이디 및 비밀번호가 틀렸습니다.')
                        location.href = '/'
                    </script>
                '''
        else:
            return f'''
                    <script>
                        alert('등록되지 않은 아이디입니다.')
                        location.href = '/'
                    </script>
                '''
    else:
        return render_template('login.html')


jwt_blocklist = set()


@main.route('/logout')
@jwt_required(locations=["cookies"])
def logout():
    delete_token(escape(session['user_id']))
    session.pop('user_id', None)

    token = get_jwt()
    jti = token['jti']
    jwt_blocklist.add(jti)

    resp = make_response('''
                        로그아웃을 성공하였습니다! <a href='/'>홈으로</a>이동하세요!
                    ''')
    resp.set_cookie('user_access_token', '', expires=0)  # 쿠키 만료 시간을 0으로 설정하여 삭제

    return resp
