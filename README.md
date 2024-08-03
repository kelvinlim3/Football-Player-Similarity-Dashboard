# Football Player Similarity

A comprehensive framework designed to quantify the technical similarity between football players using big data analytics. This tool enables users to compare one or two query players based on various criteria, such as trait importance, filters (seasons, leagues, primary positions, age, total minutes played, and overall rating), and outputs the top 20 similar players. The framework also provides visualizations, including radar charts and difference bar charts, to compare players at three levels of granularity.

## Contents

- **`Experiments/`**: Contains files used during experimentation and evaluation phases.
- **`Final/`**: Includes all necessary files to run the interactive dashboard.
- **`Reports/`**: Project documentation and reports.

## Dependencies

This framework requires the following:

- **Python**: 3.8.0
- **Dash**: 2.6.1
- **Dash-Bootstrap-Components**: 1.2.1
- **Plotly**: 5.10.0
- **Pandas**: 1.4.4
- **Numpy**: 1.23.3

## Setup and Usage

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/Football-Player-Similarity.git
   cd Football-Player-Similarity
   ```

2. **Prepare the Data**

   - Navigate to the `Final` folder.
   - Run the following command to preprocess the data:

     ```bash
     python preprocess_data.py
     ```

3. **Launch the Dashboard**

   - After preprocessing, start the interactive dashboard with:

     ```bash
     python launch_dashboard.py
     ```

   - Follow the instructions in the console output to open the dashboard in your web browser.
   - The application will be available at http://localhost:8080/.

4. **Explore the Dashboard**

   - Use the dashboard to input query players and adjust the filters to find similar players.
   - Visualize player comparisons through radar charts and difference bar charts.

## Notes

- Ensure that all dependencies are installed. You can use a virtual environment to manage these dependencies effectively.
- For further customization and feature enhancements, refer to the documentation in the `Reports/` folder.
