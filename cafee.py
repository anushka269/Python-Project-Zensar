from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
from datetime import date, datetime
from decimal import Decimal

# Database Connection
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="cafe_sys"
        )
    except mysql.connector.Error as e:
        raise Exception(f"Database connection failed: {e}")

# Custom JSON Encoder for Decimal and Date Handling
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

# HTTP Request Handler
class CafeRequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, status, message):
        """Helper function to send JSON responses."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())

    def do_GET(self):
        db = None
        try:
            db = connect_to_db()
            cursor = db.cursor(dictionary=True)

            # Handle endpoints
            if self.path == '/menu':
                cursor.execute("SELECT * FROM MenuItems")
                result = cursor.fetchall()
            elif self.path == '/inventory':
                cursor.execute("SELECT * FROM Inventory")
                result = cursor.fetchall()
            elif self.path == '/orders':
                cursor.execute("SELECT * FROM Orders")
                result = cursor.fetchall()
            else:
                self.send_json_response(404, {"error": "Endpoint not found"})
                return

            # Serialize with custom JSON encoder
            response_body = json.dumps(result, cls=CustomJSONEncoder)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
        finally:
            if db:
                db.close()


    def do_POST(self):
        db = None
        try:
            db = connect_to_db()
            cursor = db.cursor()

            # Read and parse POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            # Handle endpoints
            if self.path == '/add_menu_item':
                query = "INSERT INTO MenuItems (ItemName, Category, Price) VALUES (%s, %s, %s)"
                cursor.execute(query, (data['name'], data['category'], data['price']))
                db.commit()
                self.send_json_response(201, {"message": "Menu item added successfully"})
            elif self.path == '/place_order':
                query = "INSERT INTO Orders (ItemID, Quantity, OrderDate) VALUES (%s, %s, CURDATE())"
                cursor.execute(query, (data['item_id'], data['quantity']))
                db.commit()
                self.send_json_response(201, {"message": "Order placed successfully"})
            else:
                self.send_json_response(404, {"error": "Endpoint not found"})
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
        finally:
            if db:
                db.close()

# Run Server
def run(server_class=HTTPServer, handler_class=CafeRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run()
