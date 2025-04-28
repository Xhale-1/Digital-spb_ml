from flask import Flask, jsonify, render_template, request
import eval

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods = ["POST"])
def analyze():
    
    result = {"response":["Error: wrong request"]}
    incoming_data = request.get_json()
    print(incoming_data)
    if request.method == "POST":
        line = request.get_json()["line"]
        result = {"response":eval.inference(line)}
        print(result)

    #result = {"response": ["Принято: " + incoming_data.get("query", "")]}
    
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)