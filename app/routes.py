from flask import Blueprint, render_template, jsonify, send_file, request, send_from_directory
from app.services.s3_service import list_files, download_file
from app.services.redis_service import get_files_by_tag
from io import BytesIO

def setup_routes(app) -> None:
    """
    Set up all the routes for the Flask application.

    This function registers routes for the gallery, retrieving photos 
    via an API endpoint, and downloading images from S3.

    :param app: The Flask application instance.
    """
    
    @app.route('/')
    def gallery() -> 'render_template':
        """
        Render the gallery HTML page.

        This route serves the gallery page to the user, which includes 
        a UI for displaying the photos.

        :returns: The rendered gallery page.
        """
        return render_template('gallery.html')

    @app.route('/api/photos')
    def get_photos() -> 'jsonify':
        """
        API endpoint to fetch a list of photos by tag from S3.

        This route handles the requests to retrieve a list of photos 
        from S3 storage. It supports pagination via a continuation token
        and allows setting the number of files to be fetched via the 
        'limit' query parameter.

        :returns: JSON response with a list of photos and a continuation token.
        """
        try:
            limit = int(request.args.get('limit', 12))
            offset = int(request.args.get('offset', 0))
            tag = request.args.get('tag', 'all')

            if tag == 'all':
                response = list_files(offset=offset, limit=limit)
            else:
                object_keys=get_files_by_tag(tag=tag)
                response = list_files(offset=offset, limit=limit, object_keys=object_keys)
            return jsonify(response)
        except Exception as e:
            print(f"Error fetching photos: {e}")
            return jsonify({"files": [], "total": 0}), 500

    @app.route('/download/<path:filename>')
    def download(filename: str) -> 'send_file':
        """
        API endpoint to download a file from S3.

        This route retrieves a file from S3 storage and sends it as a downloadable 
        response to the client. The file is sent as an attachment with its original 
        filename. If the file cannot be retrieved, an error message is returned.

        :param filename: The name of the file to be downloaded.

        :returns: Sends the file as an attachment.
        """
        try:
            file_content = download_file(filename)
            if file_content:
                return send_file(
                    BytesIO(file_content),
                    as_attachment=True,
                    download_name=filename
                )
        except Exception as e:
            print(f"Error downloading file: {e}")
            return "Internal server error", 500

    @app.route('/favicon.ico')
    def robots_txt() -> 'send_from_directory':
        return send_from_directory(app.static_folder, 'favicon.ico')
    
    @app.errorhandler(404)
    def page_not_found(e) -> 'render_template':
        return render_template('404.html'), 404
    