from flask import render_template
from . import blog


@blog.route('/')
def hello_world():
    return render_template('index.html')


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