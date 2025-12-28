# Football Player Similarity Dashboard

A comprehensive framework designed to quantify the technical similarity between football players using big data analytics. This tool enables users to compare one or two query players based on various criteria, such as trait importance, filters (seasons, leagues, primary positions, age, total minutes played, and overall rating), and outputs the top 20 similar players. The framework also provides visualizations, including radar charts and difference bar charts, to compare players at three levels of granularity.

The dashboard is hosted live [here](https://football-player-similarity-dashboard.onrender.com) for demo purposes.

## Setup and Usage

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kelvinlimwan/Football-Player-Similarity-Dashboard.git
   cd Football-Player-Similarity-Dashboard
   ```

2. **Install Dependencies**

   - Use the `requirements.txt` file to install the necessary packages. Run this command in your terminal:

     ```bash
     pip install -r requirements.txt
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
   - Visualise player comparisons through radar charts and difference bar charts.

