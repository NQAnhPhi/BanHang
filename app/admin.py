from app import app, db
from app.models import DanhMuc, SanPham, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask import redirect
import utils
from flask import request

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class SanPhamView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    column_filters = ['TenSP', 'Gia']
    column_list = [
        'TenSP',
        'SoLuong',
        'Gia',
        'NgayBan',
        'fk_MaDM'
    ]
    column_labels = {
        'TenSP': 'Tên SP',
        'SoLuong': 'Số lượng',
        'MoTa': 'Mô tả',
        'Gia': 'Giá',
        'Hinh': 'Hình đại diện',
        'TinhTrang': 'Tình trạng',
        'NgayBan': 'Ngày bán',
        'fk_MaDM': 'Danh mục'
     }
    form_columns = ('TenSP', 'SoLuong', 'MoTa', 'Gia', 'Hinh', 'TinhTrang', 'NgayBan', 'fk_MaDM')

class DanhMucView(AuthenticatedModelView):
    column_display_pk = True
    column_searchable_list = ['TenDM']
    column_labels = {
        'id': 'Mã Danh mục',
        'TenDM': 'Tên Danh mục'
    }

class UserView(AuthenticatedModelView):
    can_edit = False
    can_view_details = True
    can_export = True
    column_filters = ['TenUser', 'UserName']
    column_list = [
        'TenUser',
        'UserName',
        'Email',
        'SDT',
        'DiaChi',
        'TinhTrang'
    ]
    column_labels = {
        'TenUser': 'Tên người dùng',
        'UserName': 'Tên tài khoản',
        'DiaChi': 'Địa chỉ',
        'Avatar': 'Hình đại diện',
        'TinhTrang': 'Tình trạng',
        'NgayVao': 'Ngày vào'
    }

class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        return self.render('admin/stats.html',
                           stats=utils.product_stats(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.category_stats())

admin = Admin(app=app, name="QUẢN TRỊ CỬA HÀNG", template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(DanhMucView(DanhMuc, db.session, name='Danh mục'))
admin.add_view(SanPhamView(SanPham, db.session, name='Sản phẩm'))
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
