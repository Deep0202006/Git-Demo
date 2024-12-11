import qrcode

def generate_qr_code(data, filename):
    # Create a QR Code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code grid
        border=4,  # Thickness of the border (minimum is 4)
    )
    
    # Add data to the QR Code
    qr.add_data(data)
    qr.make(fit=True)  # Fit the QR code to the data

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save(filename)
    print(f"QR Code generated and saved as {filename}")

# Example usage
if __name__ == "__main__":
    data = "https://www.example.com"  # The data you want to encode
    filename = "qrcode.png"  # The filename to save the QR code image
    generate_qr_code(data, filename)