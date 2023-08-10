from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Disable favicon handling
#@app.route('/favicon.ico')
#def favicon():
#    return app.send_static_file('favicon.ico')

# Sample data to return as JSON
sample_data = {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com"
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(sample_data)


@app.route('/')
def index():
    return render_template('testCode.html', data=sample_data)

# Ignore favicon requests to prevent 404 errors
#@app.after_request
#def ignore_favicon(response):
#    if request.path == '/favicon.ico':
#        return app.response_class(response='', status=204)
#    return response


if __name__ == '__main__':
    app.run(debug=True)
