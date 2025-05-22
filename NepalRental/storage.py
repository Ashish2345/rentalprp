# storage.py (in your project root or app directory)
import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
from urllib.parse import urljoin

@deconstructible
class CloudinaryStorage(Storage):
    def __init__(self, **settings):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name='dliqrslp0',
            api_key='728446114843378',
            api_secret='Kv6YJx2wzWCef96tRR8Hd_qdTdE',
            secure=True
        )

    def _save(self, name, content):
        """Save file to Cloudinary and return the public_id"""
        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                content,
                public_id=self._get_public_id(name),
                resource_type='auto',  # Auto-detect file type
                folder='django_uploads'  # Optional: organize in folders
            )
            return upload_result['public_id']
        except Exception as e:
            raise Exception(f"Error uploading to Cloudinary: {str(e)}")

    def _open(self, name, mode='rb'):
        """Retrieve file from Cloudinary"""
        url = self.url(name)
        import urllib.request
        response = urllib.request.urlopen(url)
        return ContentFile(response.read())

    def delete(self, name):
        """Delete file from Cloudinary"""
        try:
            cloudinary.uploader.destroy(name)
        except:
            pass  # File might not exist

    def exists(self, name):
        """Check if file exists in Cloudinary"""
        try:
            cloudinary.api.resource(name)
            return True
        except:
            return False

    def url(self, name):
        """Return the URL for accessing the file"""
        if not name:
            return ''

        url, _ = cloudinary_url(
            name,
            secure=True,
            quality='auto',
            fetch_format='auto'
        )
        return url

    def size(self, name):
        """Return file size"""
        try:
            resource = cloudinary.api.resource(name)
            return resource.get('bytes', 0)
        except:
            return 0

    def _get_public_id(self, name):
        """Generate a public_id from filename"""
        # Remove file extension and create a clean public_id
        import os
        base_name = os.path.splitext(name)[0]
        # Replace spaces and special chars with underscores
        clean_name = ''.join(c if c.isalnum() or c in '._-' else '_' for c in base_name)
        return clean_name