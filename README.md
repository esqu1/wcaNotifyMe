# WCA NotifyMe

The biggest frustration of signing up for WCA competitions is not finding out about them in time. 
An even bigger frustration, however, is when you do find out about a competition, but then 
get shut out of registration!

**WCA NotifyMe** serves to alleviate that frustration. Simply sign up for notifications
and you'll be notified when it's time to register for your next competition!

## Running the program (Development)

To run the program,
1. In Terminal, run `pip install -r requirements.txt`
2. `python run.py` to start the Flask app.
3. Go to `http://localhost:5000` in your browser to view the website!

## In production

The Flask app is controlled by `mod_wsgi` and Apache 2.4. Create a file
`server.wsgi` and have it import the `app` and `sched` objects in the application.
A sample file is shown below:

```python
#!/usr/bin/python
import sys
sys.path.insert(0,"/path/to/this/repo")
from notifyme import app as application
from notifyme import sched as scheduler
```