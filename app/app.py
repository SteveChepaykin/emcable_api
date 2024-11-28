from flask import Flask, jsonify
import pandas as pd
import psycopg2
import config
import os

app = Flask(__name__)

psql = psycopg2.connect(host=config.host, port = 15432, database=config.database, user=config.user, password=config.password)

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
    cursor.close()
    res = jsonify(results)
    # pd.DataFrame(results).to_csv(f'linedata{tagid}.csv', index=False)
    writetocsv(res, f'linedata{tagid}.csv')

    with open(f'linedata{tagid}.csv', 'r') as file:
        return res

def __custor2map(ll: list) -> dict:
    r = {}
    r['layer'] = ll[0]
    r['archive_itemid'] = ll[1]
    r['source_time'] = ll[2]
    r['value'] = ll[3]
    return r

def writetocsv(results, name):
    df = pd.DataFrame(results)
    df.to_csv(name, index=False)

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    PORT = os.environ.get('SERVER_PORT', '8880')
    app.run(host=HOST, port=PORT, debug=True)