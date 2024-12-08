from flask import Flask, render_template, request

app = Flask(__name__)

def convert_to_feet(value, unit):
    conversion_factors = {
        'cm': 0.0328084,
        'mm': 0.00328084,
        'inches': 0.0833333,
        'ft': 1,
        'm': 3.28084,
        'yd': 3
    }
    return value * conversion_factors[unit]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        length1 = float(request.form['length1'])
        length2 = float(request.form['length2'])
        width1 = float(request.form['width1'])
        width2 = float(request.form['width2'])
        unit = request.form['unit']

        # Convert all dimensions to feet
        length1 = convert_to_feet(length1, unit)
        length2 = convert_to_feet(length2, unit)
        width1 = convert_to_feet(width1, unit)
        width2 = convert_to_feet(width2, unit)

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
    except KeyError:
        return "Invalid input. Please ensure all fields are filled out correctly."
    except ValueError:
        return "Invalid input. Please enter numeric values."

if __name__ == '__main__':
    app.run(debug=True)