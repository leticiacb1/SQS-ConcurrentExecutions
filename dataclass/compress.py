from zipfile import ZipFile

class CompressFile():

    def run(self, lambda_filename : str , compress_filename: str) -> None :
        with ZipFile(compress_filename, mode='w') as zf:
            zf.write(lambda_filename)

        print("\n    [INFO] File compressed successfully.\n")
        print("\n           > Compress filename : " + compress_filename)