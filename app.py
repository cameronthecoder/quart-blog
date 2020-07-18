# THIS DOESN't work because the templates and static folders
# need to be in the quart_blog folder
# ALSO THE CURRENT_APP DOESN'T WORK
from quart_blog import create_app
app = create_app()
app.run()