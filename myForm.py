from wtforms import Form, BooleanField, StringField
from wtforms.validators import Regexp, Optional

re = {
    'id_pw': [Regexp('^\\w{1,30}$', message='Only numbers, letters and _ available. Max length 30.')],
    'l_pw': [Regexp('^\\w{0,30}$', message='Only numbers, letters and _ available. Max length 30.')],  # 允许为空
    'un': [Regexp('^[\\x21-\\x7E]{1,30}$', message='Only visible ASCII character available. Max length 30.')],
    'p': [Regexp('[137]')],
    'ISBN': [Regexp('^[\\x21-\\x7E]{1,20}$', message='Only visible ASCII character available. Max length 20.')],
    # 'na_au': [Regexp(R"(^[\x21-\x21\x23-\x7E]{1,60}$)",
    #                  message='Only visible ASCII character, except for \" available. Max length 60.')],
    # 'kw': [Regexp(R"(^[\x21-\x21\x23-\x7E]{1,60}$)",
    #               message='Only visible ASCII character, except for \" available. Max length 60.'),
    #        Regexp(R"(([^\|]+\|)*[^\|]+)", message='\"|\" can\'t appear at the start or end.')],
    'na_au': [],
    'kw': [],
    'int': [Regexp("^[1-9]{1,10}$", message='Only positive integer numbers available. Max length 10.')],
    'db': [Regexp(R"(^(?=.{1,13}$)\d*(\.\d*)?$)", message='Only positive float numbers available. Max length 13.'),
           Regexp("^(?!\\.$).*$", message='\".\" is unavailable.')]
}


class LoginForm(Form):
    user_id = StringField('user_id', validators=re['id_pw'])
    password = StringField('password', validators=re['l_pw'])


class RegisterForm(Form):
    user_id = StringField(validators=re['id_pw'])
    password = StringField(validators=re['id_pw'])
    user_name = StringField(validators=re['un'])


class AddUserForm(Form):
    user_id = StringField(validators=re['id_pw'])
    password = StringField(validators=re['id_pw'])
    privilege = StringField(validators=re['p'])
    user_name = StringField(validators=re['un'])


class ModifyPasswordForm(Form):
    user_id = StringField(validators=re['id_pw'])
    current_password = StringField(validators=re['l_pw'])
    new_password = StringField(validators=re['id_pw'])


class DeleteForm(Form):
    user_id = StringField(validators=re['id_pw'])


class ShowForm(Form):
    show_info = StringField(validators=[Optional()])
    ISBN = StringField(validators=re['ISBN'])
    name = StringField(validators=re['na_au'])
    author = StringField(validators=re['na_au'])
    keyword = StringField(validators=re['kw'])

    def validate(self, extra_validators=None):
        super().validate()
        self.ISBN.errors.clear()
        self.name.errors.clear()
        self.author.errors.clear()
        self.keyword.errors.clear()
        if self.show_info.data:
            data = self.show_info.data
            if data == 'ISBN':
                if not self.ISBN.validate(self):
                    return False
            elif data == 'name':
                if not self.name.validate(self):
                    return False
            elif data == 'author':
                if not self.author.validate(self):
                    return False
            elif data == 'keyword':
                if not self.keyword.validate(self):
                    return False
        return True


class SelectForm(Form):
    ISBN = StringField(validators=re['ISBN'])


class BuyForm(Form):
    ISBN = StringField(validators=re['ISBN'])
    quantity = StringField(validators=re['int'])


class ModifyForm(Form):
    chk_ISBN = BooleanField()
    chk_name = BooleanField()
    chk_author = BooleanField()
    chk_keyword = BooleanField()
    chk_price = BooleanField()
    ISBN = StringField(validators=re['ISBN'])
    name = StringField(validators=re['na_au'])
    author = StringField(validators=re['na_au'])
    keyword = StringField(validators=re['kw'])
    price = StringField(validators=re['db'])

    def validate(self, extra_validators=None):
        super().validate()
        chk_boxes = [self.chk_ISBN.data, self.chk_name.data, self.chk_author.data, self.chk_keyword.data,
                     self.chk_price.data]
        if not any(chk_boxes):
            self.ISBN.errors = ['At least choose one!']
            self.name.errors = ['At least choose one!']
            self.author.errors = ['At least choose one!']
            self.keyword.errors = ['At least choose one!']
            self.price.errors = ['At least choose one!']
            return False

        self.ISBN.errors.clear()
        self.name.errors.clear()
        self.author.errors.clear()
        self.keyword.errors.clear()
        self.price.errors.clear()

        flag = False
        if self.chk_ISBN.data:
            if not self.ISBN.validate(self):
                flag = True
        if self.chk_name.data:
            if not self.name.validate(self):
                flag = True
        if self.chk_author.data:
            if not self.author.validate(self):
                flag = True
        if self.chk_keyword.data:
            if not self.keyword.validate(self):
                flag = True
        if self.chk_price.data:
            if not self.price.validate(self):
                flag = True
        if flag:
            return False
        return True


class ImportForm(Form):
    quantity = StringField(validators=re['int'])
    total_cost = StringField(validators=re['db'])


class ShowFinanceForm(Form):
    count = StringField(validators=[re['int'][0], Optional()])


class LogForm(Form):
    show_info = StringField()
