
from flask import Flask, render_template

# Khởi tạo Flask
app = Flask(__name__)

# Hàm xử lý request
@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='192.168.1.93', debug=False)
