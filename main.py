import os
import sys
import platform
import http.server
import socketserver
import urllib.parse

OUTPUT = False
OUTPUT_PATH = "output.txt"
if len(sys.argv) > 1:
    if sys.argv[1] == "-p":
        PORT = int(sys.argv[2])

    if len(sys.argv) > 3:
        if sys.argv[3] == "-o":
            OUTPUT = True
            if len(sys.argv) > 4:
                OUTPUT_PATH = sys.argv[4]

else:
    PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map[".html"] = "text/html"


class MyHandler(Handler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(body)
        clipboard_text = form_data['clipboard'][0]
        clipboard_text = clipboard_text.replace('\r\n', '\n')

        print("------------ Received Text ------------")
        print(clipboard_text)

        if OUTPUT:
            with open(OUTPUT_PATH, "w") as file:
                file.writelines(clipboard_text)

            print(f"file {OUTPUT_PATH} saved!")

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return Handler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    if platform.system() == "Linux":
        os.system("ifconfig")
    elif platform.system() == "Windows":
        os.system("ipconfig")

    try:
        print("Serving at port...", PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    print("\nstopping server...")
    httpd.server_close()
