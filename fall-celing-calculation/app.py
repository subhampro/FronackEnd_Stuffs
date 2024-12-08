from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    length1 = float(request.form['length1'])
    length2 = float(request.form['length2'])
    width1 = float(request.form['width1'])
    width2 = float(request.form['width2'])

    # Calculate the number of rods and their lengths
    horizontal_rods = max(length1, length2)
    vertical_rods = max(width1, width2)
    num_horizontal_rods = int(horizontal_rods / 2) + 1
    num_vertical_rods = int(vertical_rods / 2) + 1

    return render_template('result.html', 
                           num_horizontal_rods=num_horizontal_rods, 
                           num_vertical_rods=num_vertical_rods, 
                           horizontal_rods=horizontal_rods, 
                           vertical_rods=vertical_rods)

if __name__ == '__main__':
    app.run(debug=True)