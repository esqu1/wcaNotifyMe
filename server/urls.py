from server import app

@app.route('/')
def main():
    return "Hello World"


@app.route('/submitted', methods=['POST'])
def submit():
	return 'submitted'