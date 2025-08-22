from flask import render_template


def initialize_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('general/error.html',error_code=404, error_message="Page not found"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('general/error.html', error_code=403, error_message="Access forbidden"), 403
