from pdf_privacy_redactor import PDF_Privacy_Redactor
import os

redactor = PDF_Privacy_Redactor()


# Get File Input
input_file = input("Source Path: ")
while not os.path.exists(input_file):
    print("[ERROR]: Invalid Path Entered")
    input_file = input("Source Path: ")

# Loading document
redactor.loadDocument(input_file)

# Add some patterns
print("Enter TOKENs that you want to redact!! (Type '!q' to continue)")
token = input(f"Token[{len(redactor.tokens)}]:")
while token != "!q":
    redactor.addPattern(token)
    token = input(f"Token[{len(redactor.tokens)}]:")

# Print patterns
print("Tokens List:", redactor.listPattern())

# Identify patterns
print("Identify:", redactor.identify())

# Redact all matches
redactor.redact()

# Saving document
output_file = input("Output Destination (with file_name):")
redactor.saveDocument(output_file)