import os
import base64
from flask import jsonify
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO

class BarcodeGenerator:
    @staticmethod
    def generate_barcode(isbn):
        if not isbn:
            return jsonify({"error": "ISBN is required"}), 400
        print(f"Generating barcode for ISBN: {isbn}")

        try:
            # Create a unique code for the barcode
            unique_code = f"GMSSSS SAFIDON-({len(isbn)})-{isbn}"
            barcode_stream = BytesIO()
            barcode_instance = Code128(unique_code, writer=ImageWriter())
            barcode_instance.write(barcode_stream)

            # Save the barcode image to a file
            save_dir = r'D:\Project\Library-Management-System-Backend\barcodes'  # Update this path
            os.makedirs(save_dir, exist_ok=True)
            barcode_file_path = os.path.join(save_dir, f"{isbn}.png")
            with open(barcode_file_path, 'wb') as f:
                f.write(barcode_stream.getvalue())

            # Convert the barcode image to base64 for immediate display
            barcode_stream.seek(0)  # Reset the stream position
            barcode_base64 = base64.b64encode(barcode_stream.getvalue()).decode('utf-8')

            return jsonify({
                "message": "Barcode generated and saved successfully.",
                "barcodeImage": barcode_base64,
                "barcodeFilePath": barcode_file_path,
                "status": "success"
            })

        except Exception as e:
            print(f"Exception in generate_barcode: {e}")
            return jsonify({"message": str(e), "status": "error"}), 500
