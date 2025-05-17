#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install Flask


# ### Step #1: Exploring the dataset
# Before building the Dash app, we need to explore the dataset. We recommend doing this in JupyterLab/Notebook. Since it has an interactive interface, we can easily code and examine the outputs.
# 
# First, we’ll import two libraries (please install them if you haven’t):
# 
# pandas: for loading and manipulating datasets
# plotly.express: for generating data visualizations
# Dash is built on top of plotly, so it’s easy to put plotly figures into Dash apps. This is why we are using plotly, instead of other Python data visualization libraries

# In[2]:


import pandas as pd
import plotly.express as px


# We’ll use the Avocado Prices dataset to build our example dashboard. So let’s load it and take a look at its summary.

# In[3]:


df = pd.read_csv('avocado-updated-2020.csv')

df.info()


# Now suppose we want to present the average prices of different types of avocados for various geographies across time, i.e., we want to focus on presenting the information of the columns date, average_price, type, and geography.
# 
# Let’s explore these columns more. What are the different type and geography of avocados? Let’s take a look at the categories using the value_counts method. This will show us the unique categories for these variables.
# 
# From the results below, you can see that there are two categories of type, and many different categories for geography.

# In[4]:


print(df['type'].value_counts(dropna=False))
print(df['geography'].value_counts(dropna=False))


# Since there are only two avocados types, we can plot their average_price time series on the same line chart. Let’s try creating such a figure when geography is ‘Los Angeles’.

# In[5]:


msk = df['geography'] == 'Los Angeles'

px.line(df[msk], x='date', y='average_price', color='type')


# This is a nice chart, but it’s only for one geography of ‘Los Angeles’.
# 
# How can we make it easy for users to explore this information from different geography?
# 
# If we have a dropdown with geography options, the users would be able to choose among them. Then according to the geography selected by the users, we can display the above line plot to them for that specific geography.
# 
# This is something we can do easily with Dash!

# ### Step #2: Preparing to build the Dash app
# 
# 
# The code snippets below need to be combined and run as a single Python script. We are breaking them down into pieces so that it’s easier to explain. You can either type them into your Python file or copy and paste the complete version, which will be provided in the last step of this tutorial.
# 
# First, we need to import the libraries. The necessary ones for our dashboard are:
# 
# dash: the Dash library, which includes:
# - Dash: class Dash
# - html (Dash HTML Components module): for building the layout, which contains components for every HTML tag, such as the H1 heading
# - dcc (Dash Core Components module): for building the layout, which contains various higher-level components such as dropdown and graph
# - Input, Output: for defining callback functions
# pandas: loading and manipulating the data
# plotly.express: creating figures
# 
# Then we can load the dataset as a pandas DataFrame, which is the same as earlier. Please make sure you’ve saved this Python script and the dataset avocado-updated-2020.csv in the same directory to avoid setting the path in the read_csv function.

# In[6]:


from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

avocado = pd.read_csv('avocado-updated-2020.csv')


# We’ll also create a Dash app object called app. This app is what we’ll be focusing on for the rest of the tutorial.

# In[7]:


app = Dash()


# ### Step #3: Building the layout of the dashboard
# The app-building process always starts from the layout. So first, we need to design the look of the dashboard.
# 
# The layout has the structure of a tree of components. And we use the keyword layout of the app to specify its layout. Then, using the two modules: html and dcc, we can display three components on our dashboard, from top to down:
# 
# - an H1 heading (html.H1) as the dashboard’s title. We specify its children property to be the text ‘Avocado Prices Dashboard’
# - a dropdown menu (geo_dropdown, which is a dcc.Dropdown) based on the geography
# We’ve built it as a variable outside and then referenced it within the layout:
# – options: this property specifies the options of unique geographies the dropdown has
# – value: this property is the selected geography when we first launch the app. We made it as ‘New York’
# - a graph (dcc.Graph) with id ‘price-graph’
# Below is the code to set up the layout.

# In[8]:


geo_dropdown = dcc.Dropdown(options=avocado['geography'].unique(),
                            value='New York')

app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    geo_dropdown,
    dcc.Graph(id='price-graph')
])


# As you might have noticed, we are using an html.Div component to hold our three Dash components. The html.Div is a container component, which is always used when we have multiple Dash components in the layout. We put the other Dash components as a list inside its children property.
# 
# After setting up the dashboard’s look, it’s time to add a callback function to make it interactive.

# ### Step #4: Adding interactivity to the dashboard
# The callback functions are Python functions. They get automatically called by Dash whenever their inputs change. As a result, the functions run and update their outputs.
# 
# The two main sections of the callback function are:
# 
# - decorator, which starts with @app.callback
# - function itself, which begins with def
# Below is the code of our callback function to make the plotly figure dependent on the dropdown.

# In[9]:


@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date', y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


# Within the decorator @app.callback, we specify the Output and the Input objects of the callback function. They are both the properties of Dash components.
# 
# In our example, the output is the figure property of the Dash component with id = ‘price-graph’, which is the dcc.Graph component set in the layout. While the input is the value property of the Dash component with the variable name geo_dropdown, which is the dcc.Dropdown component set in the layout. So you’ve seen two ways of specifying components in the callback function:
# 
# - pass the ID to component_id
# - pass the variable name directly to component_id, in which case Dash autogenerates IDs for the component
# 
# After specifying them, we use them within the function below. Within the parenthesis after the def update_graph, we name the input as selected_geography. This corresponds to the Input(component_id=geo_dropdown, component_property='value'). Then within the body of the function, we ask the function to:
# 
# - generate a filtered dataset filtered_avocado based on selected_geography
# - create a plotly line figure called line_fig based on this filtered dataset
# 
# The function returns this line_fig as the output, which corresponds to Output(component_id='price-graph', component_property='figure').
# 
# Here is an example. When the user selects ‘Los Angeles’ in the dropdown component, its value property will become ‘Los Angeles’, which means the input of the function selected_geography='Los Angeles'. This change will trigger the callback function, and update the output, as the line figure is only for Los Angeles.
# 
# That’s all the work needed for the callback function!
# 
# We are ready to run the dashboard.

# ### Step #5: Running the dashboard
# By default, the Dash app runs on our local computers. To complete the script, we need to add code to run the server. We can add these two lines of code after the callback function.

# In[10]:


if __name__ == '__main__':
    app.run_server(debug=True)


# And that’s it!
# 
# As mentioned earlier, we need to run all the code as a whole script.

# In[11]:


# Import libraries
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
avocado = pd.read_csv('avocado-updated-2020.csv')

# Create the Dash app
app = Dash()

# Set up the app layout
geo_dropdown = dcc.Dropdown(options=avocado['geography'].unique(),
                            value='New York')

app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    geo_dropdown,
    dcc.Graph(id='price-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date', y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




