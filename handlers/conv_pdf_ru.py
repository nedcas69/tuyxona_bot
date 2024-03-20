from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode import  qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF


def createBarCodes(barcode_value, txt):
    """
    Create barcode examples and embed in a PDF
    """
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c = Canvas(f"{barcode_value}.pdf")
    c.setFont("Verdana", 18)
    txtx = txt
    # canvas.drawString(72, 11 * 72, txtx)
    t = c.beginText(72, 11 * 72)
    t.textLines(txtx)
    c.drawText(t)
    # draw a QR code
    qr_code = qr.QrCodeWidget(barcode_value)
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(45, 45, transform=[145. / width, 0, 0, 145. / height, 0, 0])
    d.add(qr_code)
    renderPDF.draw(d, c, 15, 405)
    c.save()

