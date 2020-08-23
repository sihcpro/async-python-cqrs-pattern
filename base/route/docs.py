from sanic.response import HTTPResponse


def setup_docs_route(app, docs_url, route_url="/"):
    @app.route(route_url)
    async def docs_route(request):
        with open("./lib/base/route/default_page.html", "r+") as f:
            default_page = f.read()
            default_page = default_page.replace("{docs_url}", docs_url)
            return HTTPResponse(default_page)
