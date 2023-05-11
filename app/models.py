from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from app import app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin

class DanhMuc(db.Model):
    __tablename__ = 'danhmuc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenDM = Column(String(30), nullable=False)
    sanphams = relationship('SanPham', backref='danhmuc', lazy=False)

    def __str__(self):
        return self.TenDM

class SanPham(db.Model):
    __tablename__ = 'sanpham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenSP = Column(String(50), nullable=False)
    SoLuong = Column(Integer, nullable=False)
    MoTa = Column(String(500))
    Gia = Column(Float, default=0, nullable=False)
    Hinh = Column(String(100))
    TinhTrang = Column(Boolean, default=True)
    NgayBan = Column(DateTime, default=datetime.now(), nullable=False)
    fk_MaDM = Column(Integer, ForeignKey(DanhMuc.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='sanpham', lazy=True)

    def __str__(self):
        return self.TenSP

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenUser = Column(String(50), nullable=False)
    UserName = Column(String(50), nullable=False, unique=True)
    Password = Column(String(50), nullable=False)
    Avatar = Column(String(100))
    Email = Column(String(50))
    SDT = Column(String(20), nullable=False)
    DiaChi = Column(String(100), nullable=False)
    TinhTrang = Column(Boolean, default=True)
    NgayVao = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.TenUser

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    sanpham_id = Column(Integer, ForeignKey(SanPham.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()

    dm1 = DanhMuc(TenDM='Máy tính bộ')
    dm2 = DanhMuc(TenDM='Màn hình máy tính')
    dm3 = DanhMuc(TenDM='Linh kiện máy tính')
    dm4 = DanhMuc(TenDM='Phụ kiện máy tính')
    dm5 = DanhMuc(TenDM='Phụ kiện laptop')
    dm6 = DanhMuc(TenDM='Phụ kiện tiện ích')
    dm7 = DanhMuc(TenDM='Thiết bị âm thanh')


    with app.app_context():
        db.session.add(dm1)
        db.session.add(dm2)
        db.session.add(dm3)
        db.session.add(dm4)
        db.session.add(dm5)
        db.session.add(dm6)
        db.session.add(dm7)
        db.session.commit()

    sanphams = [
        {
            "TenSP": "PC Phong Vũ Office 30066 Intel",
            "SoLuong": 30,
            "MoTa": "Cấu hình gồm CPU Intel Core i3-10105, Mainboard PRIME H510M-K, Ram 8GB (1x8GB) DDR4 3200Mhz, SSD 250GB M.2 2280 PCIe Gen 4.0 NVMe,PSU 500W GTX580, Case PV-880B (Black)",
            "Gia": 6000000,
            "Hinh": "images/office30066.jpg",
            "fk_MaDM": 1
        }, {
            "TenSP": "Màn hình LCD ACER KA272",
            "SoLuong": 30,
            "MoTa": "Thông số: Kích thước: 27'' (1920 x 1080), Tỷ lệ 16:9, Tấm nền IPS, Góc nhìn: 178 (H) / 178 (V), Tần số quét: 75Hz , Thời gian phản hồi 1 ms, Hiển thị màu sắc: 16.7 triệu màu, Công nghệ đồng bộ: FreeSync, Cổng hình ảnh: , 1 x HDMI 1.4, 1 x VGA/D-sub",
            "Gia": 3390000,
            "Hinh": "images/LCD_ACER_KA272.jpg",
            "fk_MaDM": 2
        }, {
            "TenSP": "CPU INTEL Core i5-12400",
            "SoLuong": 30,
            "MoTa": "Thông số: Socket: 1700, Intel Core thế hệ thứ 12, Tốc độ: 2.50 GHz - 4.40 GHz (6nhân, 12 luồng), Bộ nhớ đệm: 18MB, Chip đồ họa tích hợp: Intel UHD Graphics 730",
            "Gia": 4890000,
            "Hinh": "images/INTEL_Core_i5-12400.jpg",
            "fk_MaDM": 3
        }]

    for sp in sanphams:
        spham = SanPham(TenSP=sp['TenSP'], SoLuong=sp['SoLuong'], MoTa=sp['MoTa'], Gia=sp['Gia'], Hinh=sp['Hinh'],
                        fk_MaDM=sp['fk_MaDM'])
        with app.app_context():
            db.session.add(spham)
            db.session.commit()