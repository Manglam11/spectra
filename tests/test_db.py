from src.db_manager import MySQLManager

db = MySQLManager()
db.connect()
db.log_upload("titanic.csv", 891,12, "session_001")
print(db.get_upload_history())
db.save_report("EDA", "outputs/titanic_eda.html",1)
db.disconnect()