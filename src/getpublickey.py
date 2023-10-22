import argparse
import hashlib
import http.server
import json
import socket
import ssl
import urllib.parse
import urllib.request


def get_server_certificate_info(url):
    try:
        # Ensure the URL is in the correct format
        if not url.startswith("https://"):
            url = f"https://{url}"

        # Parse the URL to extract the hostname and port
        parsed_url = urllib.parse.urlsplit(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443

        # Create an SSL context without certificate verification
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Establish an SSL/TLS connection to the server
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get the server's certificate
                server_cert = ssock.getpeercert(binary_form=True)

                # Convert the DER-encoded certificate to PEM format
                pem_cert = ssl.DER_cert_to_PEM_cert(server_cert)

                # Calculate SHA-1 fingerprint
                sha1_fingerprint = hashlib.sha1(server_cert).hexdigest()
                sha1_fingerprint = ":".join(
                    sha1_fingerprint[i : i + 2]
                    for i in range(0, len(sha1_fingerprint), 2)
                )

                certificate_info = {
                    "fingerprint": sha1_fingerprint,
                    "certificate": pem_cert,
                }

                return certificate_info

    except Exception as e:
        print("An error occurred:", str(e))
        certificate_info = {
            "error": str(e),
        }

        return certificate_info


class PublicKeyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path.lstrip("/?url=")

        try:
            # Fetch the public key information
            public_key_info = get_server_certificate_info(url)

            # Send the public key information as JSON response
            self.send_response(200)
            self.send_header(
                "Content-type", "application/json"
            )  # Set content type to JSON
            self.end_headers()

            # Serialize the public_key_info dictionary to JSON
            json_response = json.dumps(public_key_info)

            # Send the JSON response
            self.wfile.write(json_response.encode("utf-8"))
        except Exception as e:
            # Handle errors and send an error response
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode("utf-8"))


def run_server(port, host, keyfile, certfile):
    server_address = (host, port)

    httpd = http.server.HTTPServer(server_address, PublicKeyHandler)

    # Create an SSL context to enable HTTPS
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print(f"Server listening on {host}:{port}")
    httpd.serve_forever()


def run_cli(url):
    try:
        # Fetch the public key information
        certificate_info = get_server_certificate_info(url)

        # Convert the certificate_info dictionary to JSON and pretty print to stdout
        json_output = json.dumps(certificate_info, indent=4)
        print(json_output)

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="getpublickey HTTP RESTful Server and CLI",
        epilog="Author: Yaacov Zamir\nLicense: Apache License 2.0",
    )

    parser.add_argument(
        "--port", type=int, default=8443, help="Port for the HTTP server (default 8443)"
    )
    parser.add_argument(
        "--listen",
        default="0.0.0.0",
        help="Address to listen on for the HTTP server (default 0.0.0.0)",
    )
    parser.add_argument(
        "--tls-key",
        default="tls.key",
        help="Path to the TLS key file for HTTPS (default tls.key)",
    )
    parser.add_argument(
        "--tls-crt",
        default="tls.crt",
        help="Path to the TLS certificate file for HTTPS (default tls.crt)",
    )
    parser.add_argument("--url", help="URL to use in the CLI (optional)")

    args = parser.parse_args()

    if args.url:
        run_cli(args.url)
    else:
        run_server(args.port, args.listen, args.tls_key, args.tls_crt)
