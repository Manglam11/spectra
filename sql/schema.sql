USE defaultdb;

CREATE TABLE uploads_info (
    upload_id      INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    dataset_name   VARCHAR(100),
    row_count      INT,
    col_count      INT,
    uploaded_on    DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id     VARCHAR(200)
);

CREATE TABLE reports (
    report_id    INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    report_type  VARCHAR(20),
    report_path  VARCHAR(200),
    upload_id    INT,
    FOREIGN KEY (upload_id) REFERENCES uploads_info(upload_id)
);