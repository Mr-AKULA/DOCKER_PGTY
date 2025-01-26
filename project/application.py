from flask import Flask, render_template
import json
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from influxdb_client import InfluxDBClient, Point, WriteOptions

# Parameters for connecting to InfluxDB
bucket = "eee"
org = "AKULA1"
token = "XDBtANrCelRK0vXOYd0yTkMDF2YPZsM_i2Y88ZUmSWIZXMTkoDRtYCMgfAb3D6icLsVegYVeVCwhNYGmnQdQvg=="
url = "http://localhost:8086"

# Create an InfluxDB client instance
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the main page
@app.route("/")
def render_results():
    try:
        # Get column names and metrics data
        columns_names, data_metrics = metrics_data()

        # Generate JSON for the bar graph
        graph_metrics_JSON = bar_graph_JSON()

        # Generate JSON for the line graph
        graph_prediction_JSON = line_graph_JSON()

        # Render the index.html template with the generated data
        return render_template('index.html',
                               graph_prediction_JSON=graph_prediction_JSON,
                               graph_metrics_JSON=graph_metrics_JSON,
                               data_metrics=data_metrics,
                               columns_names=columns_names)
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to generate JSON for the line graph
def line_graph_JSON():
    try:
        # Flux query to get the data
        query = """
        from(bucket: "eee")
          |> range(start: 2024-04-18T00:00:00Z, stop: 2024-04-18T00:02:00Z)
          |> filter(fn: (r) => r["_measurement"] == "sensors_data_prediction")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """
        print("Flux Query:", query)  # Debug message

        # Execute the query and get the tables
        tables = query_api.query(query, org=org)
        print("Tables received:", tables)  # Debug message

        # Initialize lists to store column names and index values
        columns = set()
        for table in tables:
            for record in table.records:
                for key in record.values.keys():
                    if key not in ["_start", "_stop", "_time", "result", "table"]:
                        columns.add(key)

        indexes = []  # List to store index values (timestamps)
        for table in tables:
            for record in table.records:
                indexes.append(record.get_time())  # Get the timestamp
            break  # Exit after processing the first table

        # Create a DataFrame to store data from InfluxDB
        infl_data_df = pd.DataFrame(columns=list(columns), index=pd.to_datetime(indexes))
        # Fill the DataFrame with data from the records
        for table in tables:
            for record in table.records:
                for key in record.values.keys():
                    if key not in ["_start", "_stop", "_time", "result", "table"]:
                        infl_data_df.at[record.get_time(), key] = record.values[key]

        # Close the InfluxDB client connection
        client.close()

        # Set the index name of the DataFrame
        infl_data_df.index.name = 'time'
        # Create a line plot using Plotly
        fig_line_plot = px.line(infl_data_df)
        # Update the layout of the line plot
        fig_line_plot.update_layout(
            autosize=False,  # Disable automatic resizing
            width=900,  # Set the width of the plot
            height=500  # Set the height of the plot
        )
        # Convert the plot to JSON format for rendering
        graph_prediction_JSON = json.dumps(fig_line_plot, cls=plotly.utils.PlotlyJSONEncoder)

        # Return the JSON representation of the line plot
        return graph_prediction_JSON
    except Exception as e:
        raise RuntimeError(f"Error generating line graph JSON: {str(e)}")

# Function to generate JSON for the bar graph
def bar_graph_JSON():
    try:
        # Get metrics data
        columns_names, data_metrics = metrics_data()

        # Print column names for debugging
        print("Columns in metrics data:", columns_names)

        # Check if the 'r2' column exists in the metrics data
        if 'r2' in data_metrics.columns:
            secondary_metric = 'r2'
        else:
            secondary_metric = None

        # Create a bar plot for MAE (Mean Absolute Error)
        fig_bar_plot = px.bar(data_metrics, y='mae')

        # Add a secondary bar plot for r2 values if available
        if secondary_metric:
            fig_bar_plot.add_trace(go.Bar(x=data_metrics.index, y=data_metrics[secondary_metric],
                                          name='Secondary Value', yaxis='y2'))
            # Update the layout of the bar plot
            fig_bar_plot.update_layout(
                autosize=False,  # Disable automatic resizing
                width=500,  # Set the width of the plot
                height=500,  # Set the height of the plot
                yaxis=dict(title='MAE'),  # Title for the primary y-axis
                yaxis2=dict(title=secondary_metric, overlaying='y', side='right'),  # Title for the secondary y-axis
                barmode='group'  # Group the bars
            )
        else:
            # Update the layout of the bar plot without the secondary y-axis
            fig_bar_plot.update_layout(
                autosize=False,  # Disable automatic resizing
                width=500,  # Set the width of the plot
                height=500,  # Set the height of the plot
                yaxis=dict(title='MAE'),  # Title for the primary y-axis
                barmode='group'  # Group the bars
            )

        # Convert the plot to JSON format for rendering
        graph_metrics_JSON = json.dumps(fig_bar_plot, cls=plotly.utils.PlotlyJSONEncoder)

        # Return the JSON representation of the bar plot
        return graph_metrics_JSON
    except Exception as e:
        raise RuntimeError(f"Error generating bar graph JSON: {str(e)}")

# Function to get metrics data from InfluxDB
def metrics_data():
    try:
        # Flux query to get the data
        query = """
        from(bucket: "eee")
          |> range(start: 2024-04-18T00:00:00Z, stop: 2024-04-18T00:02:00Z)
          |> filter(fn: (r) => r["_measurement"] == "sensors_data_prediction")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """
        print("Flux Query:", query)  # Debug message

        # Execute the query and get the tables
        tables = query_api.query(query, org=org)
        print("Tables received:", tables)  # Debug message

        # Initialize lists to store column names and index values
        columns = set()
        for table in tables:
            for record in table.records:
                for key in record.values.keys():
                    if key not in ["_start", "_stop", "_time", "result", "table"]:
                        columns.add(key)

        indexes = []  # List to store index values (timestamps)
        for table in tables:
            for record in table.records:
                indexes.append(record.get_time())  # Get the timestamp
            break  # Exit after processing the first table

        # Create a DataFrame to store data from InfluxDB
        infl_data_df = pd.DataFrame(columns=list(columns), index=pd.to_datetime(indexes))
        # Fill the DataFrame with data from the records
        for table in tables:
            for record in table.records:
                for key in record.values.keys():
                    if key not in ["_start", "_stop", "_time", "result", "table"]:
                        infl_data_df.at[record.get_time(), key] = record.values[key]

        # Close the InfluxDB client connection
        client.close()

        # Set the index name of the DataFrame
        infl_data_df.index.name = 'time'
        # Return the column names and metrics data
        return list(columns), infl_data_df
    except Exception as e:
        raise RuntimeError(f"Error reading metrics data: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
