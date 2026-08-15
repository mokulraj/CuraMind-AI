from storages.backends.s3 import S3Storage


class CuraMindStaticStorage(S3Storage):
    """
    S3 storage backend for static assets.
    """

    location = "static"
    default_acl = None
    file_overwrite = True
    querystring_auth = False


class CuraMindMediaStorage(S3Storage):
    """
    Private S3 storage backend for healthcare media.
    """

    location = "media"
    default_acl = None
    file_overwrite = False
    querystring_auth = True