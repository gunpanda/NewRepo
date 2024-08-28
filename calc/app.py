import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_m2', methods=['POST'])
def run_m2():
    result = subprocess.run(['python', 'm2.py'], capture_output=True, text=True)
    return render_template('index.html', m2_output=result.stdout)

if __name__ == '__main__':
    app.run(debug=True)
