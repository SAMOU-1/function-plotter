from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

SAFE_NAMES = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "log": math.log, "exp": math.exp,
    "pi": math.pi, "e": math.e, "abs": abs
}

@app.route("/plot", methods=["POST"])
def plot():
    data = request.get_json()
    expr = data.get("expr", "")
    x_min = float(data.get("x_min", -10))
    x_max = float(data.get("x_max", 10))
    steps = int(data.get("steps", 200))

    points = []
    step = (x_max - x_min) / steps
    for i in range(steps + 1):
        x = x_min + i * step
        try:
            y = eval(expr, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})
            if isinstance(y, (int, float)) and math.isfinite(y):
                points.append({"x": round(x, 4), "y": round(y, 4)})
        except Exception:
            continue

    return jsonify({"points": points})

if __name__ == "__main__":
    app.run(debug=True, port=5000)