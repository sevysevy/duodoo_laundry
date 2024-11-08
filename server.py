from waitress import serve
    
from duodoo_laundry.wsgi import application
    
if __name__ == '__main__':
    serve(application, port='80')