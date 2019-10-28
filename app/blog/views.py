from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from . import blog
from .. import db
from .forms import PostForm
from ..models import Article, PyNews
import datetime


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


@blog.route('/about')
def about():
    return render_template('about.html')


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


@blog.route('/edit/<article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    """
    新增或编辑文章内容
    """
    form = PostForm()
    page_data = None

    if form.validate_on_submit():

        if article_id != 'new':
            page_data = Article.query.filter_by(id=article_id).first()

            page_data.title = form.title.data
            page_data.text = form.text.data
            page_data.modified_date = datetime.datetime.now()

            db.session.commit()
            flash('Edit Saved.', category='success')

        else:
            title = form.title.data
            text = form.text.data
            date = datetime.datetime.now()
            new_article = Article(title=title,
                                  text=text,
                                  create_time=date)

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

        return render_template('editor/contents_edit.html', form=form, post=page_data)

    else:
        form.title.data = ''
        form.text.data = ''

        return render_template('editor/contents_edit.html', form=form, post=page_data)


@blog.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    """
    删除选定的文章并重定向本页
    """
    res = Article.query.filter_by(id=article_id).first()
    db.session.delete(res)
    db.session.commit()

    return redirect(url_for('blog.contents'))


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