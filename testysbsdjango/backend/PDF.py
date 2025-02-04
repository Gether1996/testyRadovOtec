from viewer.models import Test, Question, PinCode, EmailInPV31, LectorPin, Course
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak, Frame, PageTemplate
from reportlab.lib import colors
from PyPDF2 import PdfMerger
import json
import os


def open_pdf(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        course = get_object_or_404(Course, hash=json_data['course_hash'])
        pins = PinCode.objects.filter(course_pin=course).order_by('order')

        # Create first PDF in memory
        buffer1 = BytesIO()
        doc1 = SimpleDocTemplate(buffer1, pagesize=letter)

        # Add course name and PIN
        styles = getSampleStyleSheet()
        formatted_date = course.start.strftime("%d.%m.%Y")
        course_info = Paragraph(f"{course.name}<br/>{formatted_date}<br/>PIN: {course.pin}", styles['Title'])

        data = [["Poradie", "Meno a Priezvisko", "PIN"]]
        data_no_lines = [["Kurz", "Poradie", "PIN"]]

        for pin in pins:
            data.append([
                f"{pin.order}." if pin.order is not None else '',
                pin.name_surname if pin.name_surname else '',
                pin.pin
            ])

            data_no_lines.append([
                f"{course.name}, {formatted_date}",
                f"{pin.order}.",
                pin.pin
            ])

        table = Table(data, colWidths=[0.1 * doc1.width, 0.6 * doc1.width, 0.3 * doc1.width], rowHeights=30)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        table_no_lines = Table(data_no_lines, colWidths=[0.15 * doc1.width, 0.15 * doc1.width, 0.15 * doc1.width],
                               rowHeights=50)
        table_no_lines.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ]))

        doc1.build([course_info, table, PageBreak()])

        # Save the first PDF
        buffer1.seek(0)
        temp_path1 = os.path.join(settings.MEDIA_ROOT, f'{course.pin}_pins_part1.pdf')
        with open(temp_path1, 'wb') as f:
            f.write(buffer1.getvalue())

        # Create second PDF in memory
        buffer2 = BytesIO()
        doc2 = SimpleDocTemplate(buffer2, pagesize=letter)
        frame_left = Frame(x1=doc2.leftMargin, y1=doc2.bottomMargin, width=doc2.width / 3, height=doc2.height,
                           showBoundary=0)

        page_template = PageTemplate(frames=[frame_left])
        doc2.addPageTemplates([page_template])

        doc2.build([table_no_lines])

        # Save the second PDF
        buffer2.seek(0)
        temp_path2 = os.path.join(settings.MEDIA_ROOT, f'{course.pin}_pins_part2.pdf')
        with open(temp_path2, 'wb') as f:
            f.write(buffer2.getvalue())

        # Merge PDFs
        merger = PdfMerger()
        merger.append(temp_path1)
        merger.append(temp_path2)

        final_pdf_path = os.path.join(settings.MEDIA_ROOT, f'{course.pin}_pins.pdf')
        with open(final_pdf_path, 'wb') as f:
            merger.write(f)
            merger.close()

        # Clean up temporary files
        os.remove(temp_path1)
        os.remove(temp_path2)

        pdf_url = f'{settings.MEDIA_URL}{course.pin}_pins.pdf'
        return JsonResponse({'status': 'success', 'pdf_url': pdf_url})

    return JsonResponse({'status': 'error'})