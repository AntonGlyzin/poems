from firebase_admin import storage

class FireBaseStorage:
    def __init__(self):
        pass
    
    @staticmethod
    def get_publick_link(source, dist):
        bucket = storage.bucket()
        blob = bucket.blob(dist)
        blob.upload_from_filename(source)
        blob.make_public()
        return blob.public_url