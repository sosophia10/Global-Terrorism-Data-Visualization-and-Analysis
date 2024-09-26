# Global Terrorism Data Visualization and Analysis

## Overview
This project is an interactive web application that visualizes global terrorism incidents, focusing on suicide tactics. The platform utilizes data from the Global Terrorism Database (GTD) and presents it through an interactive map and dynamic analytics dashboard. Users can explore patterns in terrorist activity, analyze geographical trends, and uncover operational characteristics of terrorist organizations.

## Features
- **Interactive Map**: Visualizes terrorist incidents globally with zoom and filtering capabilities.
- **Timeline Analysis**: Displays the trends in terrorism over time, highlighting periods of increased activity.
- **Casualty and Damage Analysis**: Allows users to explore fatality rates, injuries, and property damage across different incidents.
- **Attack Type and Target Visualization**: Breaks down terrorist events by attack method and target category.

## Technologies Used
- **Frontend**:
  - **HTML/CSS/JavaScript**: Standard web technologies for building the user interface.
  - **Leaflet**: For rendering the interactive map with geographic data.
  - **Chart.js**: For creating dynamic charts and visualizations in the dashboard.
  - **AJAX**: To handle data requests and updates without refreshing the page.
  
- **Backend**:
  - **Python (Flask)**: Provides the API that processes data and serves the web application.
  - **Pandas**: For data manipulation and analysis.
  - **SQLite**: Used to store and query the terrorism dataset.

## Setup and Installation

### Prerequisites
- **Python 3.x** installed on your system.
- **Flask**, **Pandas**, **Chart.js**, and **Leaflet** libraries.
  
### Installation Steps
1. Clone the repository:
   
  ```
  git clone https://github.com/your-username/global-terrorism-viz.git
  ```

2. Navigate to the project directory:
  
  ```
  cd global-terrorism-viz
  ```

3. Install dependencies:

  ```
  pip install -r requirements.txt
  ```

4. Run the Flask server:

  ```
  python app.py
  ```

5. Open your web browser and navigate to a local host, such as:

  ```
  http://127.0.0.1:5000
  ```

## Data Source
The project uses the Global Terrorism Database (GTD) for data on terrorism incidents between 1970 and 2020. The GTD is a comprehensive dataset detailing terrorist events worldwide, including incident location, fatalities, attack methods, and responsible groups.

## Usage
- Map Exploration: Users can zoom in on regions of interest to visualize terrorist events. Clicking on a map marker reveals detailed information about each incident.
- The dashboard dynamically updates based on map interaction, showing trends such as the number of incidents over time, fatalities, and attack methods.
