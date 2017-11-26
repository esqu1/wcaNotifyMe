from notifyme import app, sched

if __name__ == '__main__':
    sched.start()
    app.run(debug=True)
