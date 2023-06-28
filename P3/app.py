from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No se seleccionó ningún archivo."
        
        try:
            df = pd.read_csv(file)
        except pd.errors.ParserError:
            return "El archivo no es un archivo CSV válido."
        
        columns = df.columns.tolist()

        # Verificar y crear la carpeta 'static' si no existe
        if not os.path.isdir('static'):
            os.mkdir('static')
        
        filepath = os.path.join('static', file.filename)
        file.save(filepath)
        
        return render_template('upload.html', columns=columns, file = file, filename = file.filename)

@app.route('/plot', methods=['POST'])
def plot():
    if request.method == 'POST':
        chart_type = request.form['chart_type']
        x_column = request.form['x_column']
        y_column = request.form['y_column']
        filename = request.form['filename']
        # variable = request.form['variable']
        # data = pd.read_csv('static/test.csv')
        # size = len(data[variable])
        
        if not chart_type:
            return "No se seleccionó un tipo de gráfico."
        
        try:
            filepath = os.path.join('static', filename)
            df = pd.read_csv(filepath)
        except pd.errors.ParserError:
            return "El archivo no es un archivo CSV válido."
        
        plt.figure(figsize=(8, 6))
        
        
        if chart_type == 'scatter':
            plt.scatter(df[x_column], df[y_column])
        elif chart_type == 'line':
            plt.plot(df[x_column], df[y_column])
        elif chart_type == 'bar':
            plt.bar(df[x_column], df[y_column])
        elif chart_type == 'barh':
            plt.barh(df[x_column], df[y_column])
        elif chart_type == 'pie':
            plt.pie(df[y_column], labels=df[x_column])
        
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        # plt.title(f'{chart_type.capitalize()} plot')
        
        # Guardar la imagen generada en un archivo
        image_path = os.path.join('static', 'plot'+'.png')
        plt.savefig(image_path)
        return render_template('image.html', image = image_path)
    
    return render_template('plot.html')



# @app.route('/plot', methods=['POST'])
# def plot():
#     chart_type = request.form['chart_type']
#     x_column = request.form['x_column']
#     y_column = request.form['y_column']
#     filename = request.form['filename']
    
#     if not chart_type:
#         return "No se seleccionó un tipo de gráfico."
    
#     try:
#         filepath = os.path.join('static', filename)
#         df = pd.read_csv(filepath)
#     except pd.errors.ParserError:
#         return "El archivo no es un archivo CSV válido."
    
#     plt.figure(figsize=(8, 6))
    
#     if chart_type == 'scatter':
#         plt.scatter(df[x_column], df[y_column])
#     elif chart_type == 'line':
#         plt.plot(df[x_column], df[y_column])
#     elif chart_type == 'bar':
#         plt.bar(df[x_column], df[y_column])
#     elif chart_type == 'barh':
#         plt.barh(df[x_column], df[y_column])
#     elif chart_type == 'pie':
#         plt.pie(df[y_column], labels=df[x_column])
    
#     plt.xlabel(x_column)
#     plt.ylabel(y_column)
#     plt.title(f'{chart_type.capitalize()} plot')
    
#     # Guardar la imagen generada en un archivo
#     image_path = os.path.join('static', 'plot'+'.png')
#     plt.savefig(image_path)
    
#     return render_template('plot.html', plot_filepath=image_path)

if __name__ == '__main__':
    app.run(debug=True)