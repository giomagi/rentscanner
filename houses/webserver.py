import BaseHTTPServer
from houses.foxtons import Foxtons
from houses.persistence import Librarian

class GetPropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write("<html><head><title>PROPERTIES</title></head>")
        self.wfile.write("<body>Properties<table>")
        
        for property in Librarian().retrieveProperties():
            self.wfile.write("<tr>" + self.render(property) + "</tr>")

        self.wfile.write("</table></body></html>")

    def render(self, property):
        return "<td>" + str(property.agent) + "</td><td>" + str(property.price) + "</td><td><a href=\"" + str(property.link) + "\">" + str(property.address) + "</a></td>"

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('192.168.1.2', 1234), GetPropertiesHandler)

    Librarian().archiveProperties(Foxtons().properties())

    print "UP"

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print "DOWN"
