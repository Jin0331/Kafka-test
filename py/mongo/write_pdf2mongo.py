from pymongo import MongoClient
import base64
import gridfs
import os

def write_new_pdf(host, port, user, passwd, path):
    client = MongoClient(host = host, port = port, username = user, password = passwd)   
    db = client["test_db"]
    fs = gridfs.GridFS(db)
    
    # Note, open with the "rb" flag for "read bytes"
    with open(path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    with fs.new_file(
        chunkSize=800000,
        filename=path) as fp:
        fp.write(encoded_string)
        
def read_pdf(host, port, user, passwd, filename):
    # Usual setup
    client = MongoClient(host = host, port = port, username = user, password = passwd)   
    db = client["test_db"]
    fs = gridfs.GridFS(db)
    # Standard query to Mongo
    data = fs.find_one(filter=dict(filename=filename))
    with open(filename, "wb") as f:
        f.write(base64.b64decode(data.read()))


if __name__ == "__main__":

    # working dir
    print(os.getcwd())

    host = input("Enter HOST IP : ")
    port = int(input("Enter PORT : "))
    user = input("Enter USER : ")
    passwd = input("Enter PASSWD : ")
    pdf_path = input("Enter PDF path : ")


    # Store PDF to Mongo
    write_new_pdf(host=host, port = port, user= user, passwd= passwd, path=pdf_path)
    
    
    # Read PDF from mongo
    #read_pdf(host= host, port = port, user= user, passwd= passwd, filename="giy036.pdf")