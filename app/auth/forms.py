#encoding=utf-8
#存储各类表单

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email,Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登陆状态')
    submit = SubmitField('登陆')

class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    username = StringField('用户名', validators =[Required(),Length(1,64),
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母数字和点')])
    password = PasswordField('密码', validators=[Required(),EqualTo('password2', message = '两次密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email= field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self, field):
        if User.query.filter_by(username= field.data).first():
            raise ValidationError('用户名已经被使用')

class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators = [Required(), Length(1,64), Email()])
    submit = SubmitField('重设密码')

class PasswordResetForm(Form):
    email = StringField('邮箱', validators = [Required(), Length(1,64),Email()])
    password = PasswordField('新密码', validators=[Required(),EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('确认新密码', validators=[Required()])
    submit =SubmitField('重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知的邮箱')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码',validators = [Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('确认新密码', validators=[Required()])
    submit = SubmitField('更新密码')

class ChangeEmailForm(Form):
    email = StringField('新邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('更新邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册.')
