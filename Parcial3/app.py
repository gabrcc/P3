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

# @app.route('/dash', methods=['GET', 'POST'])
# def dash():
#     global image_counter
#     if request.method == 'POST':
#         variable = request.form['variable']
#         data = pd.read_csv('static/test.csv')
#         columns = data.columns.tolist()
#         # size = len(data[variable])
#         # plt.bar(range(size), data[variable])
#         # imagepathbar = os.path.join('static', 'bar' + '.png')
#         # plt.savefig(imagepathbar)
#         plt.plot(data[variable])
#         image_counter += 1 
#         imagepathplot = os.path.join('static', f'plot{image_counter}' + '.png')
#         plt.savefig(imagepathplot)
#         plt.close()
#         return render_template('dash.html', imageplot = imagepathplot, columns=columns)
#     return render_template('dash.html')

@app.route('/dash', methods=['GET', 'POST'])
def dash():
    global image_counter
    if request.method == 'POST':
        variable = request.form['variable']
        data = pd.read_csv('static/test.csv')
        columns = data.columns.tolist()
        chart_type = request.form['chart_type']

        if chart_type == 'line':
            plt.plot(data[variable])
            plt.title(f'{variable} - Líneal')
        elif chart_type == 'bar':
            size = len(data[variable])
            plt.bar(range(size), data[variable])
            plt.title(f'{variable} - Barra')
        elif chart_type == 'histogram':
            plt.hist(data[variable])
            plt.title(f'{variable} - Histograma')


        image_counter += 1 
        imagepathplot = os.path.join('static', f'plot{image_counter}' + '.png')
        plt.savefig(imagepathplot)
        plt.close()
        return render_template('dash.html', imageplot = imagepathplot, columns=columns,chart_types=['line', 'bar', 'histogram'])
    
    data = pd.read_csv('static/test.csv')
    columns = data.columns.tolist()
    return render_template('dash.html', columns=columns , chart_types=['line', 'bar', 'histogram'])



if __name__ == '__main__':
    app.run(debug=True)
