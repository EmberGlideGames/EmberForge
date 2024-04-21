from flask import Flask, request, Response
from werkzeug.exceptions import HTTPException
from secret import secret
import hashlib
import hmac

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def respond():
    data = request.json
    x256_hash = request.headers.get('x-hub-signature-256', default=None)
    config = data['hook']['config']
    try:
        verify_signature(request.get_data(), secret, x256_hash)
    except HTTPException as e:
        print(e)
        return Response(status=e.status_code)
    # add logging
    # clear existing webfiles from /var/www/emberglide
    # run blag
    # push the updated files to /var/www/emberglide
    return Response(status=202)


def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")
