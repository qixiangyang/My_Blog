from flask import render_template, request
from . import blog
from faker import Faker
from .. import db
from ..models import Article, PyNews


def get_fake_data():

    fake_data_list = []
    fake = Faker(locale='zh_CN')

    for _ in range(20):
        data = dict()
        data['author'] = fake.name()
        data['title'] = fake.sentence()
        data['text'] = fake.paragraph(10)
        data['category'] = fake.word()
        data['create_time'] = fake.date()
        data['update_time'] = fake.date()
        data['upload_time'] = fake.date()
        data['other_info'] = fake.password(special_chars=False)
        fake_data_list.append(data)

    return fake_data_list


@blog.route('/pyhub')
@blog.route('/')
def py_news():
    # py_news_data = PyNews.query.all()
    # py_news_dict = [x.to_json() for x in py_news_data]

    page = request.args.get('page', 1, type=int)
    pagination = PyNews.query.order_by(PyNews.pub_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items

    now_page_data = [x.to_json() for x in posts]

    return render_template('pyhub.html', page_data=now_page_data,  pagination=pagination)

    # return render_template('pynews.html', page_data=py_news_dict)


@blog.route('/archieves', methods=['GET'])
def archieves():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items

    now_page_data = [x.to_json() for x in posts]

    return render_template('archieves.html', page_data=now_page_data, pagination=pagination)
    # return render_template('archieves.html', page_data=article_data_dict)


@blog.route('/archieves/<article_id>')
def article(article_id):
    page_data = Article.query.filter_by(id=article_id).first()
    return render_template('article_page.html', page_data=page_data)


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