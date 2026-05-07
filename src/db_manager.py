import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class MySQLManager:
    """
    Handles all database operations for Spectra.
    Manages connections and CRUD ops for uploads_info and reports tables.
    """
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.port = int(os.getenv("MYSQL_PORT"))
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        self.connection = None

    def connect(self) -> None:
        """
        Connects the mysql server to our project using 5 credentials from constructor &
        assign the result to self.connection.

        Print "Connection Established" on success
        else catch any exception and print the error.
        """
        try:
            ssl_ca = os.getenv("MYSQL_SSL_CA")

            # On Streamlit Cloud, cert content is stored as a secret
            cert_content = os.getenv("MYSQL_SSL_CERT_CONTENT")
            if cert_content:
                import tempfile
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
                tmp.write(cert_content.encode())
                tmp.close()
                ssl_ca = tmp.name

            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                ssl_ca=ssl_ca
            )
            print("Connection Established")
        except mysql.connector.Error as e:
            print("Connection failed: ", e)

    def disconnect(self) -> None:
        """
        Closes the app's connection to mysql server.

        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Connection Closed")

    def log_upload(self,dataset_name:str, row_count:int, col_count:int, session_id:str) -> None:
        """
        Insert the uploaded file info in MySQL database.

        Params:
            dataset_name: name of the dataset file you are passing
            row_count: number of rows in dataset.
            col_count: number of columns in dataset.
            session_id: token generated via streamlit.

        Shows "Upload logged successfully" if operation is successful.
        """
        try:
            cursor = self.connection.cursor()
            query = ("INSERT INTO uploads_info ("
                     "dataset_name, row_count, col_count, session_id"
                     ") VALUES (%s, %s, %s, %s)")
            values = (dataset_name, row_count, col_count, session_id)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print("Upload logged successfully")
        except mysql.connector.Error as e:
            print("Failed to log upload: ",e)

    def get_upload_history(self) -> list | None:
        """
        Fetches tha data from database to show it to user.

        Returns:
            list: tuples got from database rendered in the form of list.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM uploads_info"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print("Fetching data failed: ", e)


    def save_report(self, report_type: str, report_path: str, upload_id: int) -> None:
        """
        Writes the info about report in reports_table.

        Params:
            report_type: stores what kind of analysis was done.
            report_path: stores the file path of the saved report.
            upload_id: foreign to link with uploads_info table.

        Shows "Report data saved successfully." if operation is successful.
        """
        try:
            cursor = self.connection.cursor()
            query = ("INSERT INTO reports("
                     "report_type, report_path, upload_id"
                     ") VALUES (%s, %s, %s)")
            values = (report_type, report_path, upload_id)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print("Report data saved successfully.")
        except mysql.connector.Error as e:
            print("Can't save report data: ",e)