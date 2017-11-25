from src import app, db, sched

if __name__ == '__main__':
    sched.start()
    app.run(debug=False)