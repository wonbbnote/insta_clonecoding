from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


# @app.route('/detail')
# def detail():
#     return render_template("comment.html")
@app.route('/detail/<keyword>')
def detail(keyword):
    return render_template("comment.html", word=keyword)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)