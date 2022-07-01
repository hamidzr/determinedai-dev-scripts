#!/usr/bin/env python3

import os
import detcloud.internal.secrets

def get_certs(deployment="dev"):
    secrets = detcloud.internal.secrets.get_secrets()
    with detcloud.internal.secrets.TLSFileManager(secrets[f"{deployment}_web_tls_crt"], secrets[f"{deployment}_web_tls_key"]) as tls:
        # copy file location at tls.* to current directory
        os.system(f"cp {tls.crtFile} cert.crt")
        os.system(f"cp {tls.keyFile} cert.key")


get_certs()
