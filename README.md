# Football Player Similarity
A framework to quantify the technical similarity between football players using big data. Given one or two query players, traits importance and filters (seasons, leagues, primary positions, age, total minutes played and overall rating) on output similar players, the framework outputs the top 20 similar players and provide visualisations (radar chart and difference bar chart) to compare players at three levels of granularity.

## Contents
- The 'Experiments' folder contains files used during experimentation and evaluation.
- The 'Final' folder contains files necessary to run the interactive dashboard.
- The 'Reports' folder contains the project documentations.

## Dependencies
This framework was developed using:
- Python 3.8.0
- Dash 2.6.1
- Dash-Bootstrap-Components 1.2.1
- Plotly 5.10.0
- Pandas 1.4.4
- Numpy 1.23.3

## Usage
Clone the repository and navigate to the 'Final' folder. Open command prompt, preprocess the data using:

```console
python preprocess_data.py
```

and launch the dashboard using:

```console
python launch_dashboard.py
```

Follow the console output and open http://127.0.0.1:8888/ in your browser to display the interactive dashboard.