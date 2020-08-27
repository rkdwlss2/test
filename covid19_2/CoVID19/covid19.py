# flask 모듈 임포트
from flask import Flask, render_template, request, redirect, url_for, session
import db4
import ml
import datetime
import time
# flask 객체 생성
app = Flask(__name__)

# 시크릿키 설정
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
beta={'LG화학': 1.4, 'SK케미칼': 0.35, '고려제약': 0.98, '광동제약': 0.79, '녹십자': -0.02, '녹십자홀딩스': 0.02, '대성미생물': 1.08, '대한뉴팜': 0.01, '랩지노믹스': 0.29, '바디텍메드': 0.7, '바이오니아': 0.32, '바이오리더스': 0.33, '보령제약': 1.18, '수젠텍': 0.14, '신풍제약': 0.54, '씨젠': -0.0, '씨티씨바이오': 1.08, '아이진': 1.32, '에이프로젠제약': 0.77, '엑세스바이오': 0.14, '엔케이맥스': -0.02, '옵티팜': 1.0, '우진비앤지': 1.0, '유바이오로직스': 0.76, '유한양행': 0.66, '이글벳': 1.35, '인트론바이오': 0.97, '일성신약': 0.07, '일양약품': 0.33, '제일바이오': 1.01, '종근당': 0.9, '중앙백신': 0.8, '진매트릭스': 0.38, '진바이오텍': 1.25, '진원생명과학': -0.18, '체시스': -0.18, '코미팜': 0.08, '큐브앤컴퍼니': 1.26, '파루': 0.84, '피씨엘': 0.53, '한국콜마홀딩스': 1.11, '한미약품': 0.84, '화일약품': 1.24}
kosselect={'LG화학': 1, 'SK케미칼': 1, '고려제약': 2, '광동제약': 2, '녹십자': 1, '녹십자홀딩스': 1, '대성미생물': 2, '대한뉴팜':2, '랩지노믹스': 2, '바디텍메드': 2, '바이오니아': 2, '바이오리더스': 2, '보령제약': 1, '수젠텍': 2, '신풍제약': 1, '씨젠': 2, '씨티씨바이오': 2, '아이진': 2, '에이프로젠제약': 1, '엑세스바이오': 2, '엔케이맥스': 2, '옵티팜': 2, '우진비앤지': 2, '유바이오로직스': 2, '유한양행': 1, '이글벳': 2, '인트론바이오': 2, '일성신약': 1, '일양약품': 1, '제일바이오': 2, '종근당': 1, '중앙백신': 2, '진매트릭스': 2, '진바이오텍': 2, '진원생명과학': 1, '체시스': 1, '코미팜': 2, '큐브앤컴퍼니':2, '파루': 2, '피씨엘': 2, '한국콜마홀딩스': 1, '한미약품': 1, '화일약품': 2}
zulist=['LG화학', 'SK케미칼', '고려제약', '광동제약', '녹십자', '녹십자홀딩스', '대성미생물', '대한뉴팜', '랩지노믹스', '바디텍메드', '바이오니아', '바이오리더스', '보령제약', '수젠텍', '신풍제약', '씨젠', '씨티씨바이오', '아이진', '에이프로젠제약', '엑세스바이오', '엔케이맥스', '옵티팜', '우진비앤지', '유바이오로직스', '유한양행', '이글벳', '인트론바이오', '일성신약', '일양약품', '제일바이오', '종근당', '중앙백신', '진매트릭스', '진바이오텍', '진원생명과학', '체시스', '코미팜', '큐브앤컴퍼니', '파루', '피씨엘', '한국콜마홀딩스', '한미약품', '화일약품']
@app.route('/')
def index():
    return render_template('firstpage.html',zulist=zulist)

@app.route('/kosdaq')
def kosdaq():
    kosdaq_list = db4.get_kosdaq_list()
    return render_template('kosdaq.html', kosdaq_list=kosdaq_list)

@app.route('/jinbiotech')
def jinbiotech():
    jinbiotech_list = db4.get_jinbiotech_list()
    return render_template('jinbiotech.html', jinbiotech_list=jinbiotech_list)

@app.route('/jinbiotech_pro', methods=['POST'])
def jinbiotech_pro():
    jinbiotech_list = db4.get_jinbiotech_list()
    return render_template('jinbiotech.html', jinbiotech_list=jinbiotech_list)

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
@app.route('/action_page', methods=['post'])
def action_page():
    date=request.form['date']
    text=request.form['text']

    date=datetime.datetime.strptime(date,"%Y-%m-%d")
    date1=datetime.datetime.strptime("2020-01-02","%Y-%m-%d")
    days=int((date-date1).days)
    beta1=""
    if beta[text]:
        beta1=beta[text]
    else:
        beta1=beta1+"베타에 값없다"
    per=ml.img1(days,text,beta1,kosselect[text])
    if kosselect[text]==1:
        kospy="kospy"
    elif kosselect[text]==2:
        kospy="kosdaq"
    return render_template('jong.html',name=text,per=per,days=days,beta1=beta1,kospy=kospy)
    # return render_template('jong.html',image_file="images/jin.png")
@app.after_request
def set_response_headers(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    return r
# 앱 실행 
app.run(host='127.0.0.10', port=5000, debug=True)