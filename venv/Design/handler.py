from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def file_upload():
    # This function handles the root URL and serves the home.html template
    return render_template('file_upload.html')

@app.route('/about')
def about():
    # This function handles the /about URL and serves the about.html template
    return render_template('about.html')



@app.route('/insertProduct')
def insert_product():
    # This function handles the /about URL and serves the about.html template
    return render_template('insertProduct.html')

@app.route('/listProducts')
def list_products():
    # This function handles the /about URL and serves the about.html template
    return render_template('listProducts.html')


if __name__ == '__main__':
    app.run(debug=True)
