from waitress import serves
import server
serve (server.app, host = '0.0.0.0', port = 8080)
