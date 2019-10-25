from flask import render_template, request, flash
from flask_login import login_required
from . import blog
from .. import db
from ..models import Article, PyNews


@blog.route('/pyhub')
def pyhub():
    """
    返回Py资讯页面
    """

    page = request.args.get('page', 1, type=int)
    pagination = PyNews.query.order_by(PyNews.pub_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items

    now_page_data = [x.to_json() for x in posts]

    return render_template('pyhub.html', page_data=now_page_data,  pagination=pagination)


@blog.route('/')
@blog.route('/archives', methods=['GET'])
def archives():
    """
    返回主页和自己的文章页
    """

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('archives.html', page_data=now_page_data, pagination=pagination)


@blog.route('/archives/<article_id>')
def article(article_id):
    """
    :param article_id:
    :return: 返回单篇文章
    """
    page_data = Article.query.filter_by(id=article_id).first()
    return render_template('article_page.html', page_data=page_data)


@blog.route('/contents')
@login_required
def contents():
    """
    需要先行登陆
    :return: 返回内容列表页
    """
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('editor/contents_list.html', page_data=now_page_data, pagination=pagination)


@blog.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    """
    删除选定的文章
    :return: 返回删除后剩余的文章列表
    """

    res = Article.query.filter_by(id=article_id).first()
    db.session.delete(res)
    db.session.commit()
    flash('删除成功')

    """重新返回数据"""
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('editor/contents_list.html', page_data=now_page_data, pagination=pagination)


@blog.route('/about')
def about():
    return render_template('about.html')


@blog.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@blog.errorhandler(500)
def server_internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    blog.run(debug=True)