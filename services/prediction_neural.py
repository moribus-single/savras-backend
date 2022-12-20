import pandas as pd
import numpy as np
from plotly import graph_objs as go
import neuralprophet
from sklearn import tree, model_selection, metrics
from models.file import crud_file as cf
from models.analysis import crud_analysis as ca
from sqlalchemy.orm import Session
from os import path
import io


class PredictionNeural:
    def get_result(self, fileid: int, db: Session):
        """Получение результатов нейронного прогнозирования по сохранённым .xlsx файлам."""
        return f"data/prediction_neural_{fileid}.xlsx"

    def save_to_db(
        self,
        fileid: int,
        predictions: int,
        mse: int,
        mape: int,
        result: bytes,
        db: Session,
    ):
        """Сохранение результатов PredictionNeural в БД."""
        ca.save_result_pr_neural(fileid, predictions, mse, mape, result, db)

    def make_df(self, fileid: int, predictions: int, db: Session):
        """Cчитывание бинарного файла в датафрейм для PredictionNeural."""
        file_name = f"data/sample_{fileid}.xlsx"

        if not path.exists(file_name):
            byte_file = cf.get_file(fileid, db)
            write_obj = io.BytesIO()
            write_obj.write(byte_file[0])
            write_obj.seek(0)
            df = pd.read_excel(write_obj)
            df.to_excel(file_name)

        excel_data_main = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data_main)
        data = data.drop(columns=["Unnamed: 0.1"], axis=1)

        result = self.predict_neural(fileid, predictions, data)
        self.save_to_db(fileid, predictions, result[0], result[1], result[2], db)
        return self.get_result(fileid, db)

    def predict_neural(self, fileid: int, predictions: int, data: pd.DataFrame):
        """Функция нейронного прогнозирования по датафрейму."""
        sort_data_main = data.loc[data["channel"] == "Чаты"].drop(
            columns=[
                "Unnamed: 0",
                "tm",
                "business_line",
                "sector",
                "channel",
                "skill_group",
                "avg_time_fact",
            ],
            axis=1,
        )

        x1 = sort_data_main.ds.unique()
        y1 = sort_data_main.groupby("ds")["load_fact"].sum()

        d = {"ds": x1, "y": y1}
        df_new = pd.DataFrame(d)
        df_new.reset_index(drop=True, inplace=True)

        df_train = df_new.iloc[:-predictions]
        df_test = df_new.iloc[-predictions:]

        nprophet_model = neuralprophet.NeuralProphet()

        future_df = nprophet_model.make_future_dataframe(
            df_train, periods=predictions, n_historic_predictions=len(df_train)
        )

        forecast = nprophet_model.predict(future_df)

        mse = metrics.mean_squared_error(df_test['y'], forecast.iloc[-predictions:]['yhat1'])
        mape = metrics.mean_absolute_percentage_error(df_test['y'], forecast.iloc[-predictions:]['yhat1'])

        # Визуализация
        fig = go.Figure()
        visualise = [
            go.Scatter(x=df_new["ds"], y=df_new["y"], name="fact"),
            go.Scatter(x=forecast["ds"], y=forecast["yhat1"], name="prediction"),
            go.Scatter(x=forecast["ds"], y=forecast["trend"], name="trend"),
        ]
        fig.add_traces(visualise)
        fig.write_image(f"visualisation/prediction_neural_{fileid}.png")

        forecast.to_excel(f"data/prediction_neural_{fileid}.xlsx")

        with open(f"data/prediction_neural_{fileid}.xlsx", "rb") as file:
            forecast_b = file.read()

        return mse, mape, forecast_b
