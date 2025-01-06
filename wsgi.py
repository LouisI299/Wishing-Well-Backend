from app import create_app
from app import app
from flask import current_app

app = create_app()

if __name__ == '__main__':
    app.run()

@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append({
            'route': rule.rule,
            'methods': list(rule.methods),
            'endpoint': rule.endpoint
        })
    return {'routes': routes}, 200

if __name__ == "__main__":
    app.run()
