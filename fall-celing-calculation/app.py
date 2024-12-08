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

def convert_from_feet(value, unit):
    conversion_factors = {
        'cm': 30.48,
        'mm': 304.8,
        'inches': 12,
        'ft': 1,
        'm': 0.3048,
        'yd': 0.333333
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

        length1_in_feet = convert_to_feet(length1, unit)
        length2_in_feet = convert_to_feet(length2, unit)
        width1_in_feet = convert_to_feet(width1, unit)
        width2_in_feet = convert_to_feet(width2, unit)

        horizontal_rods = max(length1_in_feet, length2_in_feet)
        vertical_rods = max(width1_in_feet, width2_in_feet)
        num_horizontal_rods = int(horizontal_rods / 2) + 1
        num_vertical_rods = int(vertical_rods / 2) + 1

        horizontal_rods = convert_from_feet(horizontal_rods, unit)
        vertical_rods = convert_from_feet(vertical_rods, unit)

        return render_template('result.html', 
                               num_horizontal_rods=num_horizontal_rods, 
                               num_vertical_rods=num_vertical_rods, 
                               horizontal_rods=horizontal_rods, 
                               vertical_rods=vertical_rods,
                               unit=unit)
    except KeyError:
        return "Invalid input. Please ensure all fields are filled out correctly."
    except ValueError:
        return "Invalid input. Please enter numeric values."

if __name__ == '__main__':
    app.run(debug=True)