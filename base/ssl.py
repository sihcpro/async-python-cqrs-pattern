import ssl


def default_ssl(ssl_path="env/default/rds-combined-ca-bundle.pem"):
    ctx = ssl.create_default_context(cafile=ssl_path)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx
