from flask import  Flask, render_template, request, redirect
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
image_counter = 0

matplotlib.use('Agg')

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not os.path.isdir('static'):
            os.mkdir('static')
        filepath = os.path.join('static', file.filename)
        file.save(filepath)
        # return 'The file name of the uploaded file is: {}'.format(file.filename)
        return redirect('/dash')
    return render_template('index.html')


@app.route('/dash', methods=['GET', 'POST'])
def dash():
    global image_counter
    if request.method == 'POST':
        variable = request.form['variable']
        variable2 = request.form['variable2']
        data = pd.read_csv('static/test.csv')
        columns = data.columns.tolist()
        chart_type = request.form['chart_type']
        size = len(data[variable])

        if chart_type == 'line':
            plt.plot(data[variable])
            plt.title(f'{variable} - Líneal')
        elif chart_type == 'bar':
            plt.bar(range(size), data[variable])
            plt.title(f'{variable} - Barra')
        elif chart_type == 'histogram':
            plt.hist(data[variable])
            plt.title(f'{variable} - Histograma')
        elif chart_type == 'scatter':
            plt.scatter(data[variable], data[variable2])
            plt.title(f'{variable} - Scatter')
        elif chart_type == 'pie':
            count = data[variable].value_counts()
            plt.pie(count, labels=count.index)
            plt.title(f'{variable} - Pie')
        elif chart_type == 'boxplot':
            plt.boxplot(data[variable])
            plt.title(f'{variable} - BoxPlot')
        elif chart_type == 'violinplot':
            plt.violinplot(data[variable])
            plt.title(f'{variable} - ViolinPlot')
        elif chart_type == 'area':
            plt.fill_between(range(size), data[variable])
            plt.title(f'{variable} - Area')


        image_counter += 1 
        imagepathplot = os.path.join('static', f'plot{image_counter}' + '.png')
        plt.savefig(imagepathplot)
        plt.close()
        return render_template('dash.html', imageplot = imagepathplot, columns=columns,chart_types=['line', 'bar', 'histogram','scatter','pie','boxplot','violinplot','area'])
    
    data = pd.read_csv('static/test.csv')
    columns = data.columns.tolist()
    return render_template('dash.html', columns=columns , chart_types=['line', 'bar', 'histogram','scatter','pie','boxplot','violinplot','area'])



if __name__ == '__main__':
    app.run(debug=True)
