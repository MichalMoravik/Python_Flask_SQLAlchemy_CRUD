# this is a module which run my application
# "app" variable we are importing needs to exist in the package (in __init__.py)
from sqlalchemycrud import app

# Run app
if __name__ == '__main__':
    app.run(debug=True)
