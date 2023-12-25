from flask import Flask, render_template, request

import communicate
import myForm
import atexit

app = Flask(__name__)

cmd = communicate.Command()


@app.route('/')
def index():
    return render_template('welcome.html', user=cmd.current_user)


@app.errorhandler(404)
def not_found(msg):
    return render_template('notFound.html', user=cmd.current_user)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    invalid = False
    success = False
    form = myForm.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.login(form.user_id.data, form.password.data)
        if not success:
            form.user_id.errors.append('User id not found or password incorrect.')
            form.password.errors.append('User id not found or password incorrect.')
    return render_template('login.html', user=cmd.current_user, form=form,
                           invalid=invalid, success=success)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    invalid = False
    success = False
    form = myForm.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.register(form.user_id.data, form.password.data, form.user_name.data)
        if not success:
            form.user_id.errors.append('User id already exist!')
    return render_template('register.html', user=cmd.current_user, form=form, invalid=invalid, success=success)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user_page():
    if not cmd.check_privilege(3):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.AddUserForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.add_user(form.user_id.data, form.password.data, form.privilege.data,
                                        form.user_name.data)
        if not success:
            form.user_id.errors.append('User id already exist or privilege unavailable.')
            form.privilege.errors.append('User id already exist or privilege unavailable.')
    return render_template('addUser.html', user=cmd.current_user, form=form, invalid=invalid, success=success)


@app.route('/modify_password', methods=['GET', 'POST'])
def modify_password_page():
    if not cmd.check_privilege(1):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.ModifyPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.modify_password(form.user_id.data, form.current_password.data,
                                               form.new_password.data)
        if not success:
            form.user_id.errors.append('User id not found or password incorrect.')
            form.current_password.errors.append('User id not found or password incorrect.')
    return render_template('modifyPassword.html', user=cmd.current_user, form=form, invalid=invalid,
                           success=success)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if not cmd.check_privilege(7):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.DeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.delete(form.user_id.data)
        if not success:
            form.user_id.errors.append('User id not found or the user has logged in.')
    return render_template('delete.html', user=cmd.current_user, form=form, invalid=invalid, success=success)


@app.route('/logout')
def logout():
    if not cmd.check_privilege(1):
        return render_template('deny.html', user=cmd.current_user)
    cmd.logout()
    return render_template('welcome.html', user=cmd.current_user)


@app.route('/learn')
def learn():
    return render_template('用户手册.html')


@app.route('/show', methods=['GET', 'POST'])
def show():
    if not cmd.check_privilege(1):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    books = []
    form = myForm.ShowForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success, books = cmd.show(form.ISBN.data, form.name.data, form.author.data, form.keyword.data)
        if not success:
            if form.name.data:
                form.name.errors.append(
                    'Only visible ASCII character, Chinese character except for \" available. Max length 60.')
            if form.author.data:
                form.author.errors.append(
                    'Only visible ASCII character, Chinese character except for \" available. Max length 60.')
            if form.keyword.data:
                form.keyword.errors.append(
                    'Only visible ASCII character, Chinese character, except for \" and | available. Max length 60.')

    return render_template('show.html', user=cmd.current_user, form=form, invalid=invalid, success=success, books=books)


@app.route('/select', methods=['GET', 'POST'])
def select():
    if not cmd.check_privilege(3):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.SelectForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.select(form.ISBN.data)
    return render_template('select.html', user=cmd.current_user, form=form, invalid=invalid, success=success)


@app.route('/select/show', methods=['GET', 'POST'])
def select_show():
    if not cmd.check_privilege(3):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.SelectForm(request.form)
    books = []
    if request.method == 'POST':
        invalid, success, books = cmd.show(None, None, None, None)
        success = False
    return render_template('select_show.html', user=cmd.current_user, form=form, invalid=invalid, success=success,
                           books=books)


@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if not cmd.check_privilege(1):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    total_cost = ''
    form = myForm.BuyForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success, total_cost = cmd.buy(form.ISBN.data, form.quantity.data)
        if not success:
            form.ISBN.errors.append('No such books exist or no enough stock.')
            form.quantity.errors.append('No such books exist or no enough stock.')
    return render_template('buy.html', user=cmd.current_user, form=form, invalid=invalid, success=success,
                           total_cost=total_cost)


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if not cmd.check_privilege(3):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.ModifyForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.modify(form.ISBN.data, form.name.data, form.author.data, form.keyword.data,
                                      form.price.data)
        if not success:
            if form.ISBN.data:
                form.ISBN.errors.append('Invalid input.')
            if form.name.data:
                form.name.errors.append('Invalid input.')
            if form.author.data:
                form.author.errors.append('Invalid input.')
            if form.keyword.data:
                form.keyword.errors.append('Invalid input.')
        else:
            cmd.get_current_user()

    return render_template('modify.html', user=cmd.current_user, form=form, invalid=invalid, success=success)


@app.route('/import', methods=['GET', 'POST'])
def import_book():
    if not cmd.check_privilege(3):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    form = myForm.ImportForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success = cmd.import_book(form.quantity.data, form.total_cost.data)
        # if not success:
        #     form.ISBN.errors.append('No such books exist or no enough stock.')
        #     form.quantity.errors.append('No such books exist or no enough stock.')
    return render_template('import.html', user=cmd.current_user, form=form, invalid=invalid, success=success)


@app.route('/show_finance', methods=['GET', 'POST'])
def show_finance():
    if not cmd.check_privilege(7):
        return render_template('deny.html', user=cmd.current_user)
    invalid = False
    success = False
    msg = ''
    form = myForm.ShowFinanceForm(request.form)
    if request.method == 'POST' and form.validate():
        invalid, success, msg = cmd.show_finance(form.count.data)
        if not success:
            form.count.errors.append('Number must be less than the total of transactions.')
    return render_template('showFinance.html', user=cmd.current_user, form=form, invalid=invalid, success=success,
                           msg=msg)


@app.route('/log', methods=['GET', 'POST'])
def log():
    if not cmd.check_privilege(7):
        return render_template('deny.html', user=cmd.current_user)
    form = myForm.LogForm(request.form)
    success = False
    msg = ''
    if request.method == 'POST' and form.validate():
        if form.show_info.data == 'finance':
            success, msg = cmd.report_finance()
        elif form.show_info.data == 'employee':
            success, msg = cmd.report_employee()
        else:
            success, msg = cmd.log()
    return render_template('log.html', user=cmd.current_user, msg=msg, success=success)


atexit.register(cmd.end)

if __name__ == '__main__':
    app.run()
