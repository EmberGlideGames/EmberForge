Title: Git Automation!
Description: A short post on git, webhooks and automation.
Date: 2024-04-21 18:22
Tags: WIP, git, automation, webhooks

This is a short post on git, webhooks and automation to automatically update a blag page when 
a new post is committed to a GitHub repository.

## Github Setup

### Setting up a webhook

First, you need to set up a webhook in your GitHub repository. Go to the repository settings, 
then to the "Webhooks" section. Click on "Add webhook" and enter the URL where you want to receive notifications and 
ensure to set a valid secret.

<img alt="Webhook settings" src="./git-automation-photos/Git Webhooks 01.png" class="responsive">

## Server Setup
### Receiving the webhook

First we need to set up a small single route web application to receive the webhook. A minimal implementation of 
``` python
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def respond():
    return Response(status=202)
    
app.run()
```
Now we have an app that will receive and respond to the webhook. Next we need to verify the request came from a verified 
source, GitHub in this case.

A sample implementation of this using 
[python](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#python-example) 
is provided by GitHub and provided below for simplicity.

``` python  
import hmac
import hashlib
from werkzeug.exceptions import HTTPException

def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body()) <- Flask 
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")
```

Getting the needed features from the request and and verifying the signature slightly expands our script to the following.

``` python
from flask import Flask, request, Response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def respond():
    x256_hash = request.headers.get('x-hub-signature-256', default=None)
    try:
        verify_signature(request.get_data(), secret, x256_hash)
    except HTTPException as e:
        print(e)
        return Response(status=e.status_code)
    #TODO: Valid webhook, update the local files and rebuild the site
    return Response(status=202)
    
app.run()
```


#### Service files
``` shell
[Unit]
Description=Emberglide webhook receiver
Requires=emberglide_webhook.socket
After=network.target

[Service]
User=emberglide
Group=www-data
WorkingDirectory=<script working directory>
ExecStart=/home/emberglide/emberforge/venv/bin/gunicorn \
        --access-logfile - \
        --workers 1 \
        --bind unix:/run/emberglide_webhook.sock \
        wsgi:app

[Install]
WantedBy=multi-user.target

```

``` shell
[Unit]
Description=emberglide socket

[Socket]
ListenStream=/run/emberglide_webhook.sock

[Install]
WantedBy=sockets.target
```
