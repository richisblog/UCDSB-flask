from bs4 import BeautifulSoup
import re
import os

def extract_registered_or_waitlisted_blocks(html_text):
    """
    提取 CourseDetails.tXXXX = {...}; 的 JS 块中，状态为 Registered 或 Waitlist 的那些块
    :param html_text: 原始 HTML 内容
    :return: list[str]，符合条件的 script 块代码
    """
    pattern = r'CourseDetails\.(t\d+)\s*=\s*{.*?};'
    matches = re.finditer(pattern, html_text, re.DOTALL)

    selected_blocks = []
    for match in matches:
        js_code = match.group(0)
        if re.search(r'REGISTRATION_STATUS"\s*:\s*"?(Registered|Waitlist)"?', js_code):
            selected_blocks.append(js_code)

    return selected_blocks

def extract_term_code_from_input(html_content):
    """
    从 HTML 中提取 <input name="termCode" value="..."> 的值
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find('input', {'name': 'termCode'})
    if tag and tag.has_attr('value'):
        return tag['value']
    return "UNKNOWN"

def minify_schedule_html(input_path, output_path):
    """
    精简 HTML，仅保留 student_name_id、term_code 和已注册课程对象
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 提取课程对象
    selected_blocks = extract_registered_or_waitlisted_blocks(html)

    # 提取课程 ID 和 term_code
    print("✅ 保留的注册/候补课程 ID：")
    for block in selected_blocks:
        match = re.search(r'CourseDetails\.(t\d+)', block)
        if match:
            print(match.group(1))

    term_code = extract_term_code_from_input(html)
    print(f"\n🎓 学期代码 (termCode)：{term_code}")

    # 构造精简 HTML
    soup = BeautifulSoup(html, 'html.parser')
    new_soup = BeautifulSoup('<html><head><meta charset="utf-8"></head><body></body></html>', 'html.parser')
    new_body = new_soup.body

    # 添加 student_name_id
    student_div = soup.find('div', id='student_name_id')
    if student_div:
        new_body.append(student_div)

    # 添加 term_code div
    term_div = new_soup.new_tag('div', id='term_code')
    term_div.string = term_code
    new_body.append(term_div)

    # 添加 script 块
    for js_code in selected_blocks:
        script_tag = new_soup.new_tag('script')
        script_tag.string = js_code
        new_body.append(script_tag)

    # 保存输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_soup.prettify())

    print(f"\n✅ 精简完成，输出文件：{output_path}")

def generate_minified_html(original_html):
    """
    从原始 HTML 文本生成精简版 HTML（返回字符串和 term_code）
    用于 Flask 上传时直接处理内容，不经过文件路径。
    """
    selected_blocks = extract_registered_or_waitlisted_blocks(original_html)
    term_code = extract_term_code_from_input(original_html)

    soup = BeautifulSoup(original_html, 'html.parser')
    new_soup = BeautifulSoup('<html><head><meta charset="utf-8"></head><body></body></html>', 'html.parser')
    body = new_soup.body

    # 学生姓名
    student_div = soup.find('div', id='student_name_id')
    if student_div:
        body.append(student_div)

    # 学期
    term_div = new_soup.new_tag('div', id='term_code')
    term_div.string = term_code
    body.append(term_div)

    # 所有保留课程的 script 块
    for js_code in selected_blocks:
        script_tag = new_soup.new_tag('script')
        script_tag.string = js_code
        body.append(script_tag)

    return str(new_soup.prettify()), term_code

# 示例运行
if __name__ == '__main__':
    input_file = 'ss.html'
    output_file = 'Schedule_Slimmed.html'

    if os.path.exists(input_file):
        minify_schedule_html(input_file, output_file)
    else:
        print(f"❌ 找不到文件：{input_file}")
