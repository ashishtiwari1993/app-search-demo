import json
from elastic_enterprise_search import AppSearch
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

client = AppSearch(
    config['appsearch']['base_endpoint'],
    bearer_auth=config['appsearch']['api_key'])

engine = config['appsearch']['engine_name']

@app.route("/")
def home():
    data = client.search(engine_name=engine, query="", body={"page":{"size":48}})
    return render_template("CineFlix/index.html", data=data)


@app.route("/search", methods=['GET'])
def search():
    search = request.args.get('q')
    d = client.search(engine_name=engine, query=search, body={"page":{"size":48}})
    response = jsonify(d['results'])
    response.headers.add('access-control-allow-origin', '*')
    response.headers.add('access-control-allow-methods', 'get, post')
    return response

@app.route("/test", methods=['GET'])
def test():
    search = ""
    d = client.search(engine_name=engine, query="", body={"page":{"size":48},"sort":{"imdb_rating":"desc"}})
    response = jsonify(d['results'])
    response.headers.add('access-control-allow-origin', '*')
    response.headers.add('access-control-allow-methods', 'get, post')
    return response

if __name__ == "__main__":
    app.run(debug=False)
