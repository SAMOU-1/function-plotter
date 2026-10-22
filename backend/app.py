import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import re  # 用于正则表达式，把 3x 变成 3*x

app = Flask(__name__)
CORS(app)

# 允许函数里使用的数学函数和常量 (已加入高等数学函数)
SAFE_NAMES = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "arcsin": math.asin, "arccos": math.acos, "arctan": math.atan, # 反三角函数
    "sqrt": math.sqrt, "log": math.log, "exp": math.exp,
    "pi": math.pi, "e": math.e, "abs": abs
}

@app.route("/plot", methods=["POST"])
def plot():
    data = request.get_json()
    expr = data.get("expr", "")
    x_min = float(data.get("x_min", -20))
    x_max = float(data.get("x_max", 20))
    steps = int(data.get("steps", 500))

    # 智能纠错：把用户习惯的输入转换为 Python 能懂的语法
    # 例如：把 3x 变成 3*x，把 x^2 变成 x**2
    expr_fixed = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
    expr_fixed = expr_fixed.replace('^', '**')

    points = []
    step = (x_max - x_min) / steps
    for i in range(steps + 1):
        x = x_min + i * step
        try:
            # 计算 y 值
            y = eval(expr_fixed, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})
            
            # 检查 y 是不是有效的数字，且不是无限大
            if isinstance(y, (int, float)) and math.isfinite(y):
                points.append({"x": round(x, 4), "y": round(y, 4)})
        except Exception:
            continue  # 算不出来（比如除以0）就跳过

    return jsonify({"points": points})

if __name__ == "__main__":
    # 启动服务器
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))