#encoding=utf-8
#存储各类表单

from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class PostForm(Form):
    head = StringField('标题', validators=[Required(),Length(1,64)])
    category = SelectField('Category',coerce=int)
    body = PageDownField('有什么想法？', validators=[Required()])
    submit = SubmitField('提交')

class CommentForm(Form):
    username =StringField('用户名', validators=[Required()])
    body = StringField('评论区',validators=[Required()])
    submit = SubmitField('提交')

class CategoryForm(Form):
    body = StringField('标签',validators=[Required()])
    submit = SubmitField('提交')

class EditProfileForm(Form):
    name = StringField('姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('关于')
    submit = SubmitField('提交')

class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    username = StringField('用户名', validators =[Required(),Length(1,64),
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母数字和点')])
    confirmed = BooleanField('已确认')
    role = SelectField('Role', coerce=int)
    name = StringField('姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('关于')
    submit = SubmitField('提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')