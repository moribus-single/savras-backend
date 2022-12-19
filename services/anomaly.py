import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import IsolationForest
from models.file import crud_file as cf
from models.analysis import crud_analysis as ca
from sqlalchemy.orm import Session
from os import path
import io


class Anomaly:
    def get_result(self, fileid: int, with_anomaly_bool: bool, db: Session):
        if with_anomaly_bool:
            return f"data/with_anomaly_{fileid}.xlsx"
        return f"data/without_anomaly_{fileid}.xlsx"

    def save_to_db(
        self, fileid: int, with_anomaly: bytes, without_anomaly: bytes, db: Session
    ):
        """Сохранение результатов Anomaly в БД."""
        ca.save_result_anom(fileid, with_anomaly, without_anomaly, db)

    def make_df(
        self, fileid: int, predictions: int, with_anomaly_bool: bool, db: Session
    ):
        """Cчитывание бинарного файла в датафрейм."""
        file_name = f"data/anomaly_{fileid}.xlsx"
        if not path.exists(file_name):
            byte_file = cf.get_file(fileid, db)
            write_obj = io.BytesIO()
            write_obj.write(byte_file[0])
            write_obj.seek(0)
            df = pd.read_excel(write_obj)
            df.to_excel(file_name)

        excel_data_main = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data_main)

        result = self.find_anomaly(fileid, predictions, data)
        self.save_to_db(fileid, result[0], result[1], db)
        return self.get_result(fileid, with_anomaly_bool, db)

    def find_anomaly(self, fileid: int, predictions: int, data: pd.DataFrame):
        data = data.loc[data["channel"] == "Чаты"].drop(
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
        x = data.ds.unique()
        y = data.groupby("ds")["load_fact"].sum()

        d = {"ds": x, "y": y}
        df_new = pd.DataFrame(d)
        df_new.reset_index(drop=True, inplace=True)

        train_df = df_new.iloc[:-predictions]
        test_df = df_new.iloc[-predictions:]

        df_anom = self.isolation_forest_anomaly_detection(df_new, "y", 0.15)
        df_not_anom = df_anom.loc[df_anom["y_Isolation_Forest_Anomaly"] != True]
        df_not_anom = df_not_anom.drop(columns=["y_Isolation_Forest_Anomaly"])

        df_anom.to_excel(f"data/with_anomaly_{fileid}.xlsx")
        df_not_anom.to_excel(f"data/without_anomaly_{fileid}.xlsx")

        with open(f"data/with_anomaly_{fileid}.xlsx", "rb") as file:
            df_anom_b = file.read()
        with open(f"data/without_anomaly_{fileid}.xlsx", "rb") as file:
            df_not_anom_b = file.read()

        return df_anom_b, df_not_anom_b

    def isolation_forest_anomaly_detection(self, df, column_name, percentage):
        min_max_scaler = preprocessing.StandardScaler()
        np_scaled = min_max_scaler.fit_transform(df[[column_name]])
        scaled_time_series = pd.DataFrame(np_scaled)

        model = IsolationForest(contamination=percentage)
        model.fit(scaled_time_series)

        isolation_forest_anomaly_column = column_name + "_Isolation_Forest_Anomaly"
        df[isolation_forest_anomaly_column] = model.predict(scaled_time_series)
        df[isolation_forest_anomaly_column] = df[isolation_forest_anomaly_column].map(
            {1: False, -1: True}
        )
        return df
