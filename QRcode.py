import qrcode

# Define the data you want to encode in the QR code
data = ""

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("my_qrcode.png")

print("QR Code generated successfully!")

import qrcode


# Function to generate QR code for phone number
def generate_phone_qr(phone_number, file_name):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to QR code (in this case, a tel: URL)
    qr.add_data('tel:' + phone_number)
    qr.make(fit=True)

    # Generate QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to file
    img.save(file_name)


# Example usage:
phone_number = "+1234567890"  # Replace with the phone number you want to encode
file_name = "phone_qr.png"  # Name of the output image file
generate_phone_qr(phone_number, file_name)
print(f"QR code for phone number '{phone_number}' generated and saved as '{file_name}'")
