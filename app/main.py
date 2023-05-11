import math
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
from app import app, utils, login, otp, mail
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from app.models import UserRole

@app.route("/")
def home():
    cate_id = request.args.get('DM_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)
    sanphams = utils.load_sanphams(cate_id=cate_id, kw=kw, page=int(page))
    counter = utils.dem_sanphams()
    return render_template("index.html",
                           sanphams=sanphams,
                           pages=math.ceil(counter/app.config['PAGE_SIZE']))

@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        TenUser = request.form.get('TenUser')
        UserName = request.form.get('UserName')
        Password = request.form.get('Password')
        Email = request.form.get('Email')
        SDT = request.form.get('SDT')
        DiaChi = request.form.get('DiaChi')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if Password.strip().__eq__(confirm.strip()):
                Avatar = request.files.get('Avatar')
                if Avatar:
                    res = cloudinary.uploader.upload(Avatar)
                    avatar_path = res['secure_url']

                utils.add_user(TenUser=TenUser, UserName=UserName, Password=Password, SDT=SDT,
                               DiaChi=DiaChi, Email=Email, Avatar=avatar_path)
                msg = Message('OTP', sender='phi.nqa.61cntt@ntu.edu.vn', recipients=[Email])
                msg.body = str(otp)
                mail.send(msg)
                return render_template('verify.html')
            else:
                err_msg = 'Mật khẩu không khớp !!'
        except Exception as ex:
            err_msg = 'Thông tin lỗi: ' + str(ex)

    return render_template("register.html", err_msg = err_msg)

@app.route('/validate',methods=['POST'])
def validate():
    user_otp = request.form.get('otp')
    if otp == int(user_otp):
        return redirect(url_for('user_signin'))
    return "<h3>Please Try Again</h3>"

@app.route('/user-login', methods=['get','post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        UserName = request.form.get('UserName')
        Password = request.form.get('Password')

        user = utils.check_login(UserName=UserName, Password=Password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'Tên đăng nhập hoăc mật khẩu không đúng !!'
    return render_template("login.html", err_msg=err_msg)

@app.route('/admin-login', methods=['post'])
def signin_admin():
    err_msg = ''
    UserName = request.form.get('UserName')
    Password = request.form.get('Password')

    user = utils.check_login(UserName=UserName, Password=Password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
        return redirect('/admin')
    else:
        err_msg = 'Không phải là tài khoản admin'
        return redirect(url_for("signin_admin", err_msg=err_msg))

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.route('/cart')
def cart():
    return render_template('cart.html',
                           stats=utils.count_cart(session.get('cart')))

@app.route('/api/add-cart', methods=['post'])
def add_to_card():
    data = request.json
    id = str(data.get('id'))
    TenSP = data.get('TenSP')
    Gia = data.get('Gia')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1

    else:
        cart[id] = {
            'id': id,
            'TenSP': TenSP,
            'Gia': Gia,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))
@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))
@app.route('/api/delete-cart/<sanpham_id>', methods=['delete'])
def delete_cart(sanpham_id):
    cart = session.get('cart')
    if cart and sanpham_id in cart:
        del cart[sanpham_id]
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    if 'cart' in session and session['cart']:
        utils.add_receipt(session.get('cart'))
        del session['cart']
        return jsonify({'code': 404})
    return jsonify({'code': 200})

@app.context_processor
def common_response():
    return {
        'danhmucs': utils.load_danhmucs(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
