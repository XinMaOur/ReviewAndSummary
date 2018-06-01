#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Xin
# @Time: 2018-06-01 10:16
import random
import traceback
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from flask import Flask, session, request, make_response


app = Flask(__name__)
app.config.update(
        DEBUG=True,
        SECRET_KEY='xinma'
        )

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除干扰的i, l, o,
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


class createCode():

    '''
        @todo
        @param size: 图片的大小,格式(宽, 高), 默认为(120, 30)
                     @param chars: 允许的字符集合,格式字符串
                     @param img_type: 图片保存的格式, 默认为GIF,可选的为GIF，
                     JPEG， TIFF， PNG
                     @param mode: 图片模式,默认为RGB
                     @param bg_color: 背景颜色,默认为白色
                     @param fg_color: 前景色,验证码字符颜色,默认为蓝色 # 0000FF
                     @param font_size: 验证码字体大小
                     @param font_type: 验证码字体的详细路径,默认为expo.ttf
                     @param length: 验证码字符个数
                     @param draw_lines: 是否划干扰线
                     @param n_lines: 干扰线的条数范围, 格式元组，默认为(1,
                     2),只有draw_lines为True时有效
                     @param draw_points: 是否画干扰点
                     @param point_chance: 干扰点出现的概率,大小范围[0, 100]
                     @return: [0]: PIL Image实例
                     @return: [1]: 验证码图片中的字符串

    '''

    def __init__(self):

        self.size = (120, 30)
        self.chars = init_chars
        self.img_type = "GIF"
        self.mode = "RGB"
        self.bg_color = (230, 230, 230)
        self.fg_color = (18, 18, 18)
        self.font_size = 20
        self.font_type = '/usr/share/fonts/expottf/Expo.ttf'
        self.length = 4
        self.draw_lines = True
        self.n_line = (1, 2)
        self.draw_points = True
        self.point_chance = 1

        print "into create_validate_code"
        self.width, self.height = self.size  # 宽, 高
        self.img = Image.new(self.mode, self.size, self.bg_color)  # 创建图形
        self.draw = ImageDraw.Draw(self.img)  # 创建画笔

    def get_chars(self):
        print "into get_chars"
        '''生成给定长度的字符串, 返回列表格式'''
        return random.sample(self.chars, self.length)

    def create_lines(self):
        print "create_lines"
        '''绘制干扰线'''
        line_num = random.randint(*self.n_line)  # 干扰线条数
        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            # 结束点
            end = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            self.draw.line([begin, end], fill=(0, 0, 0))

    def create_points(self):
        print "create_points"
        '''绘制干扰点'''
        chance = min(100, max(0, int(self.point_chance)))  # 大小限制在[0, 100]
        for w in range(self.width):
            for h in range(self.height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

    def create_strs(self):
        print "create_strs"
        '''绘制验证码字符'''
        c_chars = self.get_chars()
        strs = ' %s ' % ' '.join(c_chars)      # 每个字符前后以空格隔开
        font = ImageFont.truetype(self.font_type, self.font_size)
        font_width, font_height = font.getsize(strs)
        self.draw.text(((self.width - font_width) / 3, (self.height - font_height) / 3),
                  strs, font=font, fill=self.fg_color)
        return ''.join(c_chars)

    def run(self):
        if self.draw_lines:
            self.create_lines()
        if self.draw_points:
            self.create_points()
        strs = self.create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = self.img.transform(self.size, Image.PERSPECTIVE, params)  # 创建扭曲
        img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜, 边界加强(阀值更大)
        return img, strs


@app.route('/')
def index():
    return 'test'


@app.route('/code/')
def get_code():
    try:
        # 把strs发给前端, 或者在后台使用session保存
        code = createCode()
        code_img, strs = code.run()
        buf = BytesIO()
        code_img.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/gif'
        session['img'] = strs.upper()
        return response
    except Exception as e:
        print "e", traceback.format_exc(e)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if session.get('img') == request.form.get('img').upper():
            return 'OK'
        return 'Error'
    return """
    <form action="" method="post">
        <p>Name:<input type=text name=username>
        <p>Password:<input type=text name=password>
        <p>CAPTCHA:<input type=text name=img>
        <img id="verficode" src="http://0.0.0.0:18888/code"
        onclick="this.src='http://0.0.0.0:18888/code?'+Math.random()">    // onclick事件用于每次点击时获取一个新的验证码
        <p><input type=submit value=Login>
     </form>
     """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=18888, debug=True)
