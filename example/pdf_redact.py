from pdf_privacy_redactor import PDF_Privacy_Redactor

redactor = PDF_Privacy_Redactor()

# Loading document
redactor.loadDocument("document.pdf")

# Add some patterns
redactor.addPattern("security")

# Print patterns
print("Patterns:", redactor.listPattern())

# Identify patterns
print("Identify:", redactor.identify())

# Redact all matches
redactor.redact()

# Saving document
redactor.saveDocument("output.pdf")