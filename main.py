import os
import platform
import argparse
import http.server
import socketserver
import urllib.parse


PORT = 8000
OUTPUT = False
OUTPUT_PATH = "output.txt"
MESSAGE = ""

parser = argparse.ArgumentParser(description="LAN text copy paste between devices without client app (using browser)")

# Optional argument
parser.add_argument("-m", "--message", type=str,
                    help="{Text} or {Textfile Path} for send to client device")

# Optional argument
parser.add_argument("-p", "--port", type=int,
                    help="set port for listening. Default:8000")

# Optional argument
parser.add_argument("-o", "--output", type=str,
                    help="set output path to save recived text from client device into a file. Default:output.txt")

args = parser.parse_args()

# set optional port to listening
if args.port:
    PORT = args.port

# set optional output path
if args.output:
    OUTPUT = True
    OUTPUT_PATH = args.output

# set optional text message on MESSAGE
if args.message:
    MESSAGE = args.message
    
    # check MESSAGE is a File
    if os.path.isfile(MESSAGE):
        file_path = MESSAGE
        with open(file_path, 'r') as message_file:
            MESSAGE = message_file.read()


# create a message file for js
with open('message.txt', 'w') as f:
    f.write(MESSAGE)

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map[".html"] = "text/html"


class MyHandler(Handler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(body)
        clipboard_text = form_data['clipboard'][0]
        clipboard_text = clipboard_text.replace('\r\n', '\n')

        print("\n------------ Start of Received Text ------------")
        print(clipboard_text)
        print("------------ End of Received Text --------------\n")

        # save recived text in a file
        if OUTPUT:
            with open(OUTPUT_PATH, "w") as file:
                file.write(clipboard_text)

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

    # remove message.txt file
    filename = "message.txt"

    try:
        os.remove(filename)
        print(f"The file {filename} has been removed successfully.")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")
