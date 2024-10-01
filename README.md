# LR-EDA
Linear Regression Web App

# Linear Regression Web App

This web application allows users to upload a CSV file, perform a linear regression analysis, and display the results visually in a graph. The app is built using Python, Flask for the backend, and HTML/CSS for the frontend.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Features
- **File Upload**: Users can upload CSV files containing the data for analysis.
- **Linear Regression**: Perform a simple linear regression on the uploaded data and visualize the results in a scatter plot with the regression line.
- **Download Results**: Option to download the regression results as a CSV file.
- **Responsive Design**: The UI is responsive and works on both desktop and mobile devices.
- **Data Generation**: Generate random data for regression analysis from the navbar.

## Technologies Used

### Backend:
- Python
- Flask

### Frontend:
- HTML
- CSS

### Libraries:
- **Pandas**: For handling CSV files
- **Matplotlib**: For plotting the results
- **NumPy**: For performing linear regression
- **Flask**: For creating the web framework
- **CSS3**: For styling the frontend (including the navigation bar and footer)

## Setup Instructions

### Prerequisites
Ensure you have the following installed on your local machine:
- Python (version 3.6 or higher)
- pip (Python package manager)

### Installation
1. Clone this repository to your local machine:

    git clone https://github.com/Bagora/LR-EDA.git
  

2. Navigate to the project directory:

    cd LR-EDA


3. Install the required Python packages:

    pip install -r requirements.txt


## Running the Application

1. Run the Flask application:

    python app.py
