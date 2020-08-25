# flask 모듈 임포트
from flask import Flask, render_template, request, redirect, url_for, session
import db4
# flask 객체 생성
app = Flask(__name__)

# 시크릿키 설정
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    kosdaq_list = db4.get_kosdaq_list()
    return render_template('kosdaq.html', kosdaq_list=kosdaq_list)

@app.route('/member/<no>')
def member(no):
    temp_dic = db4.member(no)
    return render_template('member.html', temp_dic = temp_dic)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add')
def add():
    return render_template('add_member.html')


@app.route('/add_pro', methods=['POST'])
def add_pro():
    userID = request.form['userID']
    userName = request.form['userName']
    pwd = request.form['pwd']
    # userId 유무에 따른 분기 
    if db4.member(userID):
        return render_template('fail.html')
    else:
        db4.member_add(userID, userName, pwd)
        return render_template('success.html')

@app.route('/login_pro', methods = ['POST'])
def login_pro():
    userID= request.form['userID']
    pwd = request.form['pwd']
    result = db4.login_result(userID, pwd)
    if result:
        # userId 값을 session에 저장 
        session['userID'] = userID
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/log_out')
def log_out():
    # del session['userID']
    session.pop('userID', None)
    return redirect('/')


@app.route('/worldcity_list')
def worldcity_list() :
    worldcity_list = db4.get_worldcity_list()
    return render_template('worldcityList.html', worldcity_list=worldcity_list, totalcount = len(worldcity_list))



@app.route('/worldcity/<no>')
def worldcity(no):
    temp_dic = db4.worldcity(no)
    return render_template('worldcity.html', temp_dic = temp_dic)

@app.route('/search_worldcity_list')
def search_list() :
    worldcity_name = request.args['worldcity_name']
    worldcity_list = db4.search_worldcity_list(worldcity_name)
    return render_template('search_worldcity_list.html',worldcity_list=worldcity_list, totalcount = len(worldcity_list), worldcity_name = str(worldcity_name))

@app.route('/worldcity_add')
def worldcity_add():
    return render_template('worldcity_add.html')

@app.route('/worldcity_add_pro', methods=['post'])
def worldcity_add_pro():
    c_code = request.form['c_code']
    c_name = request.form['c_name']
    c_gnp = request.form['c_gnp']
    c_population = request.form['c_population']
    print(c_code, c_name, c_gnp, c_population)
    db4.worldcity_add(c_code, c_name, c_gnp, c_population)
    return redirect('/worldcity_list')

@app.route('/action_page', methods=['post'])
def action_page():
    date=request.form['date']
    print(date)
    return render_template('jong.html')

@app.route('/worldcity_delete/<worldcity_no>')
def worldcity_delete(worldcity_no):
    temp_dic = db4.worldcity(worldcity_no)
    return render_template('worldcity_delete.html',temp_dic = temp_dic)

@app.route('/worldcity_delete_pro/<worldcity_no>')
def worldcity_delete_pro(worldcity_no):
    db4.worldcity_delete(worldcity_no)
    return redirect('/worldcity_list')

@app.route('/member_update/<member_no>')
def member_update(member_no):
    temp_dic = db4.member(member_no)
    return render_template('member_update.html', temp_dic = temp_dic)

@app.route('/member_update_pro', methods=['post'])
def member_update_pro():
    c_no = request.form['c_no']
    c_id = request.form['c_id']
    c_pwd = request.form['c_pwd']
    db4.member_update(c_no, c_id, c_pwd)
    return redirect(url_for('member', no = int(c_no)))

@app.route('/worldcity_update/<worldcity_no>')
def worldcity_update(worldcity_no):
    temp_dic = db4.worldcity(worldcity_no)
    return render_template('worldcity_update.html',temp_dic = temp_dic)

@app.route('/worldcity_update_pro', methods=['post'])
def worldcity_update_pro():
    c_no = request.form['c_no']
    c_gnp = request.form['c_gnp']
    c_population = request.form['c_population']
    db4.worldcity_update(c_no, c_gnp, c_population)
    return redirect(url_for('worldcity', no = int(c_no)))

# 앱 실행 
app.run(host='127.0.0.10', port=5000, debug=True)