from flask import Flask, render_template, request
import os
from parser.html_parser import extract_student_id
from parser.minifier import generate_minified_html, extract_term_code_from_input
from flask_sqlalchemy import SQLAlchemy
from models import db, Student, Course



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # 文件型数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with app.app_context():
    db.init_app(app)
    db.create_all()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file.filename.endswith('.html'):
        return "❌ 只接受 HTML 文件", 400

    # 读取原始 HTML 内容
    html = file.read().decode('utf-8')

    # 提取姓名 / 学号 / 学期
    name, student_id = extract_student_id(html)
    term_code = extract_term_code_from_input(html)

    # 使用 minifier 精简 HTML
    minified_html, _ = generate_minified_html(html)

    # 重命名并保存文件
    if name and student_id:
        safe_name = name.replace(' ', '_')
        filename = f"{safe_name}_{student_id}_{term_code}.html"
    else:
        filename = file.filename

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(minified_html)

    # 渲染结果页面
    return render_template(
        'result.html',
        name=name,
        student_id=student_id,
        term_code=term_code,
        filename=filename
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
