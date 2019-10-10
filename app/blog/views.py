from flask import render_template
from . import blog
from faker import Faker


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
    return render_template('pynews.html')


@blog.route('/archieves')
def archieves():
    return render_template('archieves.html')


@blog.route('/archieves/<article_id>')
def article(article_id):
    data = get_fake_data()
    print(data)
    return render_template('article_page.html')


@blog.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@blog.errorhandler(500)
def server_internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    blog.run(debug=True)