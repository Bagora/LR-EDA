from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
import random
from faker import Faker
import time  # For generating unique filenames
import matplotlib

matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Ensure static and uploads directories exist
if not os.path.exists('static'):
    os.makedirs('static')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check if the uploaded file is CSV
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# File upload route with data preprocessing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Perform Linear Regression
        try:
            data = pd.read_csv(filepath)
            
            # Check for non-numeric columns
            numeric_data = data.select_dtypes(include=[np.number])
            
            # Ensure there are exactly 2 columns of numeric data
            if numeric_data.shape[1] != 2:
                flash('The CSV must have exactly two numeric columns.')
                return redirect(url_for('index'))
            
            X = numeric_data.iloc[:, :-1].values
            Y = numeric_data.iloc[:, -1].values
            reg = LinearRegression()
            reg.fit(X, Y)
            
            # Plotting
            plt.figure()
            plt.scatter(X, Y, color='blue')
            plt.plot(X, reg.predict(X), color='red')
            plt.title('Linear Regression')
            plt.xlabel('X')
            plt.ylabel('Y')
            plot_filepath = os.path.join('static', 'plot.png')
            plt.savefig(plot_filepath)
            
            return render_template('index.html', filename='plot.png')
        
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('index'))

    else:
        flash('Allowed file types are CSV')
        return redirect(url_for('index'))

# Route to download the plot file
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('static', filename), as_attachment=True)

@app.route('/generate', methods=['GET', 'POST'])
def generate_random_data():
    if request.method == 'GET':
        # If the request is a GET, just render the index page
        return render_template('generate_random_data.html')

    elif request.method == 'POST':
        # Handle POST request for data generation
        try:
            # Initialize Faker and random seed
            fake = Faker()
            random.seed(42)

            # Function to generate random names, ages, and salaries
            def generate_sample_data(num_samples=1000):
                data = []
                for _ in range(num_samples):
                    name = fake.name()
                    age = random.randint(25, 50)  # Generating ages between 25 and 50
                    salary = random.randint(12000, 500000)
                    data.append({"Name": name, "Age": age, "Salary": salary})
                return pd.DataFrame(data)

            # Generate random data
            sample_data = generate_sample_data(1000)
            
            # Save to CSV
            timestamp = int(time.time())  # Unique filename using timestamp
            csv_filename = f"random_data_{timestamp}.csv"
            csv_filepath = os.path.join('static', csv_filename)
            sample_data.to_csv(csv_filepath, index=False)

            # Send the CSV file for download
            return send_file(csv_filepath, as_attachment=True)
        
        except Exception as e:
            flash(f"An error occurred while generating data: {str(e)}")
            return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
