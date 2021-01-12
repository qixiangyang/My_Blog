from flask import render_template, request, flash, redirect, url_for, jsonify, Response, current_app
from sqlalchemy import and_
from flask_login import login_required
from flask_mail import Message, Mail
from functools import wraps
from . import blog
from .. import db
from .forms import PostForm, SourceForm
from ..models import (Article, PyNews, Click)
import datetime
from pathlib import Path
import random


def log_access(f):
    """
    一个装饰器，用于记录某个页面的请求信息
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now()
        func_name = f.__name__
        ip = request.remote_addr
        cookie = str(request.cookies)
        user_agent = str(request.user_agent)
        access_data = Click(route=func_name,
                            time=datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second),
                            ip_address=ip,
                            cookie=cookie,
                            user_agent=user_agent)
        try:
            db.session.add(access_data)
            db.session.commit()
        except ConnectionError as e:
            print(e)
        return f(*args, **kwargs)
    return wrapper


@blog.route('/')
@log_access
def index():
    """
    返回主页
    """
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.status != -1).order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('index.html', page_data=now_page_data, pagination=pagination)


@blog.route('/archives', methods=['GET'])
@log_access
def archives():
    """
    自己的文章页
    """

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.status != -1).order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('archives.html', page_data=now_page_data, pagination=pagination)


@blog.route('/pyhub', methods=['GET', 'POST'])
@log_access
def pyhub():
    """
    返回Py资讯页面
    提交博客地址，成功后需要有提交成功的提示信息
    后台会将提交的数据源通过邮件发送至我的邮箱
    """

    page = request.args.get('page', 1, type=int)
    pagination = PyNews.query.filter(PyNews.status != -1).order_by(PyNews.pub_time.desc()).limit(300).from_self().paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    form = SourceForm()
    if form.validate_on_submit():

        mail = Mail()
        msg = Message(subject='新的博客源',
                      recipients=['qixiangyangrm@foxmail.com'])

        msg.html = '<b>{}<b>'.format(form.blog_source.data)

        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error('邮件发送失败，请排查:{}'.format(e))
        finally:
            flash('博客源已经成功提交，博主会尽快添加，感谢支持')

    return render_template('pyhub.html', page_data=now_page_data,  pagination=pagination, form=form)


@blog.route('/about')
@log_access
def about():
    return render_template('about.html')


@blog.route('/archives/<article_id>')
@log_access
def article(article_id):
    """
    进入特定文章页
    :param article_id: 文章id
    :return: 返回单篇文章
    """
    page_data = Article.query.filter(and_(Article.id == article_id, Article.status != -1)).first()
    if page_data:
        return render_template('article_page.html', page_data=page_data)
    else:
        return render_template('404.html')


@blog.route('/contents')
@login_required
def contents():
    """
    内容管理页，返回所有的博客内容
    :return: 返回内容列表页
    """
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.update_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('editor/contents_list.html', page_data=now_page_data, pagination=pagination)


@blog.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    """
    删除选定的文章并重定向至本页
    """
    res = Article.query.filter_by(id=article_id).first()
    db.session.delete(res)
    db.session.commit()

    return redirect(url_for('blog.contents'))


@blog.route('/edit/<article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    """
    新增或编辑文章内容
    首先判断是否提交了表单，如果提交了表单，则进入表单提交的流程。
    若未提交表单，则进入读取数据的流程。
    """
    form = PostForm()
    page_data = None

    if form.validate_on_submit():

        if article_id != 'new':

            now = datetime.datetime.now()

            page_data = Article.query.filter_by(id=article_id).first()
            page_data.title = form.title.data
            page_data.text = form.text.data
            page_data.text_pre = form.text_pre.data
            page_data.update_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
            page_data.tags = form.tags.data
            page_data.category = form.category.data
            if form.save.data:
                page_data.status = -1
            else:
                page_data.status = 1
            db.session.commit()
            flash('完成编辑.', category='success')

        else:
            now = datetime.datetime.now()

            title = form.title.data
            text = form.text.data
            text_pre = form.text_pre.data
            category = form.category.data
            tags = form.tags.data
            author = '加油马德里'
            create_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
            if form.save.data:
                status = -1
            else:
                status = 1

            new_article = Article(title=title,
                                  text=text,
                                  text_pre=text_pre,
                                  category=category,
                                  tags=tags,
                                  create_time=create_time,
                                  author=author,
                                  status=status)

            db.session.add(new_article)
            db.session.flush()
            article_id = new_article.id
            db.session.commit()

            flash('文章新增成功.', category='success')

        return redirect(url_for('blog.edit', article_id=article_id))

    if article_id != 'new':

        page_data = Article.query.filter_by(id=article_id).first()

        form.title.data = page_data.title
        form.text.data = page_data.text
        form.text_pre.data = page_data.text_pre
        form.category.data = page_data.category
        form.tags.data = page_data.tags

        return render_template('editor/contents_edit.html', form=form, post=page_data)

    else:
        form.title.data = ''
        form.text.data = ''
        form.text_pre.data = ''

        return render_template('editor/contents_edit.html', form=form, post=page_data)


@blog.route('/upload/', methods=['POST'])
@login_required
def upload():
    """
    文章中需要插入图片时，使用本函数上传图片，并回传图片上传目录
    """
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        ex = file.filename.split('.')[1]
        filename = str(int(datetime.datetime.now().timestamp())) + str(random.randint(1, 1000)) + '.' + ex
        parts = ['app', 'upload', 'pic', filename]
        path = Path.cwd().joinpath(*parts)
        file.save(str(path))

        res = {
            'success': 1,
            'message': '上传成功',
            'url': url_for('.image', name=filename)
        }
    return jsonify(res)


@blog.route('/image/<name>')
def image(name):
    """
    返回文章中的图片
    """
    parts = ['app', 'upload', 'pic', name]
    path = Path.cwd().joinpath(*parts)
    with open(str(path), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp


@blog.route('/test')
def test():
    return redirect(url_for("blog.test_re", _external=True))


@blog.route('/test/redirect')
def test_re():
    return "are you ok"


@blog.errorhandler(404)
def page_not_found(e):
    """
    404页面
    """
    return render_template('404.html'), 404


@blog.errorhandler(500)
def server_internal_error(e):
    """
    500页面
    """
    return render_template('500.html'), 500


if __name__ == '__main__':
    blog.run(debug=True)