import pymysql

def connection(db, host, pswrd, port, user):
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=db,
        host=host,                                      
        password=pswrd,                                  
        read_timeout=timeout,
        port=int(port),
        user=user,                                      
    )
    cursor = connection.cursor()

    return connection
