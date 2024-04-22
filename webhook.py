import git
import hashlib
import hmac
import os
import shutil
from blag import blag
from flask import Flask, request, Response
from werkzeug.exceptions import HTTPException
from secret import secret

app = Flask(__name__)

input_dir = "./build"
output_dir = "/var/www/emberglide"

@app.route('/update', methods=['POST'])
def respond():
    x256_hash = request.headers.get('x-hub-signature-256', default=None)
    try:
        verify_signature(request.get_data(), secret, x256_hash)
    except HTTPException as e:
        print(e)
        return Response(status=e.status_code)
    # add logging
    repo = git.Repo(".")
    repo.remotes.origin.pull()
    shutil.rmtree(output_dir, ignore_errors=True)
    #for src_dir, dirs, files in reversed(os.walk(output_dir)):
    #    for file_ in files:
    #        os.remove(file_)
    #    if src_dir != output_dir:
    #        os.rmdir(src_dir)

    blag.build(blag.parse_args(["build"]))
    for src_dir, dirs, files in os.walk(input_dir):
        dst_dir = src_dir.replace(input_dir, output_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            shutil.move(src_file, dst_dir)
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
