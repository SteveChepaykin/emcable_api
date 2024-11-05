from flask import Flask, jsonify
import psycopg2
import config

app = Flask(__name__)

# Конфигурация MySQL
app.config['PSQL_HOST'] = config.host
app.config['PSQL_USER'] = config.user
app.config['PSQL_PASSWORD'] = config.password
app.config['PSQL_DB'] = config.database

psql = psycopg2.connect(host=app.config["PSQL_HOST"], port = 15432, database=app.config["PSQL_DB"], user=app.config["PSQL_USER"], password=app.config["PSQL_PASSWORD"])

@app.route('/api/data/<tagid>', methods=['GET'])
def getTableOfId(tagid: int):
    cursor = psql.cursor()
    cursor.execute(f'''
    select dr.layer, dr.archive_itemid, to_timestamp(dr.source_time / 10000000 - 11644473600) AS source_time,  dr.value
    from data_raw as dr
    where
      dr.archive_itemid = {tagid} and layer = 1
    order by dr.source_time desc
    ''')
    results = cursor.fetchall()
    psql.commit()
    cursor.close()
    res = jsonify(results)
    print(res)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432)