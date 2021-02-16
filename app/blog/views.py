from datetime import datetime, date
import random

from sqlalchemy import and_
from flask_login import login_required
from flask_mail import Message, Mail
from functools import wraps
from pathlib import Path
from flask import (render_template, request, flash, redirect, url_for, jsonify, Response, current_app)

from app import db
from app.blog import blog
from app.blog.forms import PostForm, SourceForm
from app.models import (Article, ArticleStatus, PyNews, AccessLog, Category)


def log_access(f):
    """
    一个装饰器，用于记录某个页面的请求信息
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        ip_address = request.headers.get("X-Real-Ip", None) or request.remote_addr
        access_data = AccessLog(
            route=f.__name__,
            ip_address=ip_address,
            cookie=str(request.cookies),
            user_agent=str(request.user_agent),
            request_method=request.method.lower()
        )
        current_app.logger.info(f"request_info => ip: {ip_address}, cookie: {request.user_agent}"
                                f"url: {request.url}, method: {request.method.lower()}")
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
    page_size = request.args.get('page_size', 10, type=int)

    pagination = Article.query.filter(
        Article.status == ArticleStatus.publish
    ).order_by(
        Article.create_time.desc()
    ).paginate(
        page, per_page=page_size, error_out=False
    )

    page_data = [x.json for x in pagination.items]

    return render_template('index.html', page_data=page_data, pagination=pagination)


@blog.route('/archives', methods=['GET'])
@log_access
def archives():
    """
    自己的文章页
    """

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    pagination = Article.query.filter(
        Article.status == ArticleStatus.publish
    ).order_by(
        Article.create_time.desc()
    ).paginate(
        page, per_page=page_size, error_out=False
    )

    page_data = [x.json for x in pagination.items]

    return render_template('archives.html', page_data=page_data, pagination=pagination)


@blog.route('/pyhub', methods=['GET', 'POST'])
@log_access
def pyhub():
    """
    返回Py资讯页面
    提交博客地址，成功后需要有提交成功的提示信息
    后台会将提交的数据源通过邮件发送至我的邮箱
    """

    page = request.args.get('page', 1, type=int)
    pagination = PyNews.query.filter(
        PyNews.status != -1
    ).order_by(
        PyNews.pub_time.desc()
    ).limit(300).from_self().paginate(page, per_page=20, error_out=False)
    now_page_data = [x.to_json() for x in pagination.items]

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


@blog.route('/archives/<article_id>', methods=["GET"])
@log_access
def article(article_id):
    """
    进入特定文章页
    """
    article_res = Article.query.filter(and_(
        Article.id == article_id,
        Article.status == ArticleStatus.publish
    )).first()
    if article_res:
        return render_template('article_page.html', data=article_res.json)

    return render_template('404.html')


@blog.route('/archives/<article_id>/delete', methods=["GET"])
@login_required
def delete_article(article_id):
    """
    删除选定的文章并重定向至本页
    """
    article_res = Article.query.filter_by(id=article_id).first()
    if article_res:
        article_res.status = ArticleStatus.delete
    db.session.commit()

    return redirect(url_for('blog.contents'))


@blog.route('/contents')
@login_required
def contents():
    """
    内容管理页，返回所有的博客内容
    :return: 返回内容列表页
    """
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(
        Article.status != ArticleStatus.delete
    ).order_by(
        Article.update_time.desc()
    ).paginate(page, per_page=10, error_out=False)
    now_page_data = [x.json for x in pagination.items]

    return render_template('editor/contents_list.html', page_data=now_page_data, pagination=pagination)


@blog.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    """
    新增或编辑文章内容
    首先判断是否提交了表单，如果提交了表单，则进入表单提交的流程。
    若未提交表单，则进入读取数据的流程。
    """
    form = PostForm()

    # 提交表单
    if request.form:
        title = form.title.data
        text = form.text.data
        text_pre = form.text_pre.data
        category = form.category.raw_data
        tags = form.tags.data
        status = ArticleStatus.script if form.save_script.data else ArticleStatus.publish
        create_time = form.create_time.data
        # 新增文章
        if article_id == 0:
            new_article = Article(title=title, text=text, text_pre=text_pre,
                                  status=status, author="加油马德里", create_time=create_time)
            db.session.add(new_article)
            db.session.flush()
            db.session.commit()
            new_article.creat_article_category(category_id_list=[int(x) for x in category])
            new_article.creat_article_tag(tag_name_list=tags.split(";"))
            article_id = new_article.id
            flash('文章新增成功.', category='success')

        # 编辑文章
        else:
            article_res = Article.query.filter_by(id=article_id).first()
            article_res.title = title
            article_res.text = text
            article_res.text_pre = text_pre
            article_res.status = status
            article_res.create_time = create_time
            article_res.creat_article_category(category_id_list=[int(x) for x in category])
            article_res.creat_article_tag(tag_name_list=tags.split(";"))
            db.session.commit()
            flash('保存成功.', category='success')

        return redirect(url_for('blog.edit', article_id=article_id))

    article_res = Article.query.filter_by(id=article_id).first()
    form.title.data = article_res.title if article_res else ""
    form.text.data = article_res.text if article_res else ""
    form.text_pre.data = article_res.text_pre if article_res else ""
    form.tags.data = article_res.text_pre if article_res else ""
    form.create_time.data = article_res.create_time if article_res else datetime.now()
    form.category.choices = [(x.get("category_id"), x.get("category_name")) for x in Category.get_all_category()]

    return render_template('editor/contents_edit.html', form=form, post=article_res)


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
        filename = str(int(datetime.now().timestamp())) + str(random.randint(1, 1000)) + '.' + ex
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