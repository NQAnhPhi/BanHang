from app import app, db
from app.models import DanhMuc, SanPham, User, Receipt, ReceiptDetail, UserRole
from flask_login import current_user
from sqlalchemy import func
import hashlib

def load_danhmucs():
    return DanhMuc.query.all()

def load_sanphams(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    sanphams = SanPham.query.filter(SanPham.TinhTrang.__eq__(True))

    if cate_id:
        sanphams = sanphams.filter(SanPham.fk_MaDM.__eq__(cate_id))

    if kw:
        sanphams = sanphams.filter(SanPham.TenSP.contains(kw))

    if from_price:
        sanphams = sanphams.filter(SanPham.Gia.__ge__(from_price))

    if to_price:
        sanphams = sanphams.filter(SanPham.Gia.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return sanphams.slice(start, end).all()

def dem_sanphams():
    return SanPham.query.filter(SanPham.TinhTrang.__eq__(True)).count()

def get_sanpham_by_id(sanpham_id):
    return SanPham.query.get(sanpham_id)

def add_user(TenUser, UserName, Password, SDT, DiaChi, **kwargs):
    Password = str(hashlib.md5(Password.strip().encode('utf-8')).hexdigest())
    user = User(TenUser = TenUser.strip(), UserName = UserName.strip(), Password = Password, SDT = SDT.strip(),DiaChi = DiaChi
                , Email = kwargs.get('Email'), Avatar = kwargs.get('Avatar'))
    db.session.add(user)
    db.session.commit()

def check_login(UserName, Password, role=UserRole.USER):
    if UserName and Password:
        Password = str(hashlib.md5(Password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.UserName.__eq__(UserName.strip()),
                                 User.Password.__eq__(Password),
                                 User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              sanpham_id=c['id'],
                              quantity=c['quantity'],
                              unit_price=c['Gia'])
            db.session.add(d)
        db.session.commit()

def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['Gia']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

def category_stats():
    return db.session.query(DanhMuc.id, DanhMuc.TenDM,
                            func.count(SanPham.id))\
                     .join(SanPham,
                           SanPham.fk_MaDM.__eq__(DanhMuc.id),
                           isouter=True)\
                     .group_by(DanhMuc.id, DanhMuc.TenDM).all()

def product_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(SanPham.id, SanPham.TenSP, func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
                            .join(ReceiptDetail, ReceiptDetail.sanpham_id.__eq__(SanPham.id), isouter=True)\
                            .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                            .group_by(SanPham.id, SanPham.TenSP)

    if kw:
        p = p.filter(SanPham.TenSP.contains(kw))

    if from_date:
        p = p.filter(Receipt.create_date.__ge__(from_date))

    if to_date:
        p = p.filter(Receipt.create_date.__le__(to_date))

    return p.all()