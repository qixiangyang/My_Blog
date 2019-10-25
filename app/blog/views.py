from flask import render_template, request, flash
from flask_login import login_required
from . import blog
from .. import db
from ..models import Article, PyNews


@blog.route('/pyhub')
@blog.route('/')
def pyhub():
    # py_news_data = PyNews.query.all()
    # py_news_dict = [x.to_json() for x in py_news_data]

    page = request.args.get('page', 1, type=int)
    pagination = PyNews.query.order_by(PyNews.pub_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items

    now_page_data = [x.to_json() for x in posts]

    return render_template('pyhub.html', page_data=now_page_data,  pagination=pagination)


@blog.route('/archives', methods=['GET'])
def archives():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('archives.html', page_data=now_page_data, pagination=pagination)


@blog.route('/archives/<article_id>')
def article(article_id):
    page_data = Article.query.filter_by(id=article_id).first()
    return render_template('article_page.html', page_data=page_data)


@login_required
@blog.route('/contents')
def contents():

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    now_page_data = [x.to_json() for x in posts]

    return render_template('editor/contents_list.html', page_data=now_page_data, pagination=pagination)


@login_required
@blog.route('/delete_article/<article_id>')
def delete_article(article_id):
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