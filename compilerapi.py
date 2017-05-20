from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask import jsonify
import subprocess
import urllib, os, sys
app = Flask(__name__)
api = Api(app)

class RunC(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('code', type=str, required=True, location='json')
      args = parser.parse_args(strict=True)
      code=urllib.unquote(args['code']).decode('utf8') 
      #print code
      response = []
      with open('test.c', 'w') as file:
         file.write(code)
      p = subprocess.Popen(['gcc', 'test.c', '-o', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = p.communicate()
      if os.path.exists('test.c'):
          os.remove('test.c')
      if (err):
          print "Error"
          response.append({'error':err})
          return response, 412
      print "Success"
      q = subprocess.Popen(['./test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
      (stdout, stderr) = q.communicate()
      print q.stdin.readline()
      # if sys.stdin.isatty():
#           print "Nothing in the STDIN - 2 "
#       else:
#           print "Something in the STDIN - 1"
      # response.append({'output':q})
 #      if os.path.exists('test'):
 #          os.remove('test')
 #      return response, 200
      

class RunPython(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('code', type=str, required=True, location='json')
      args = parser.parse_args(strict=True)
      code=urllib.unquote(args['code']).decode('utf8') 
      print code
      response = []
      with open('test.py', 'w') as file:
         file.write(code)
      p = subprocess.Popen(['python', 'test.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = p.communicate()
      if os.path.exists('test.py'):
          os.remove('test.py')
      if (err):
          print "Error"
          response.append({'error':err})
          return response, 412
      print "Success"
      response.append({'output':out})
      return response, 200
      
           
        
api.add_resource(RunC, '/C/')
api.add_resource(RunPython, '/python/')

if __name__ == '__main__':
    app.run(threaded=True)