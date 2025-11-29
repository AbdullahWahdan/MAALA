from reportlab.pdfgen import canvas

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Introduction to Support Vector Machines")
    c.drawString(100, 730, "SVM is a supervised machine learning algorithm.")
    c.drawString(100, 710, "It is used for classification and regression tasks.")
    c.save()

if __name__ == "__main__":
    create_dummy_pdf("test_svm.pdf")
    print("Created test_svm.pdf")
