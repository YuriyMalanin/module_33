import glob
from datetime import datetime
import os
import json
import dill
import pandas as pd

path = os.environ.get('PROJECT_PATH', '..')
def predict():
    latest_model = sorted(os.listdir(f'{path}/data/models'))[-1]
    with open(f'{path}/data/models/{latest_model}', 'rb') as f:
        model = dill.load(f)
    predicts = pd.DataFrame(columns=['car_id', 'predict'])
    for file in glob.glob(f'{path}/data/test/*json'):
        with open(file) as fin:
            form = json.load(fin)
            df = pd.DataFrame.from_dict([form])
            y = model.predict(df)
            x = {'car_id': df.id, 'predict': y}
            df1 = pd.DataFrame(x)
            predicts = pd.concat(objs=[predicts, df1], axis=0)
    print(predicts)

    predicts.to_csv(path_or_buf=f'{path}/data/predictions/predicts_{datetime.now().strftime("%Y%m%d%H%M")}.csv', index=False)

if __name__ == '__main__':
    predict()

