from flask import Flask, render_template
import webbrowser

app = Flask(__name__)


@app.route('/')
def hello_world():
    ##  return 'Hello, World!'
    return render_template('index.html')


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5001/')
    app.run(host="0.0.0.0", port=5001, debug=True)
