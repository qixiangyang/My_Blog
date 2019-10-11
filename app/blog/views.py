from flask import render_template, jsonify
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


@blog.route('/')
def hello_world():
    return render_template('index.html')


@blog.route('/about')
def about():
    return render_template('about.html')


@blog.route('/py-news')
def py_news():
    py_news_data = PyNews.query.all()
    py_news_dict = [x.to_json() for x in py_news_data]
    print(py_news_dict)
    return render_template('pynews.html', page_data=py_news_dict)


@blog.route('/archieves')
def archieves():
    page_data = get_fake_data()
    return render_template('archieves.html', page_data=page_data)


@blog.route('/archieves/<article_id>')
def article(article_id):
    page_data = get_fake_data()[0]
    with open('text.txt', mode='r', encoding='utf-8') as f:
        txt_html = f.read()
    print(page_data)
    return render_template('article_page.html', page_data=page_data, markdown_data=txt_html)


@blog.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@blog.errorhandler(500)
def server_internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    blog.run(debug=True)