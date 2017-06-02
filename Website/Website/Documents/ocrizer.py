from .cloud_ocr import CloudOCR
import argparse
import os

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='ABBYY CloudOCR')
	parser.add_argument('--application_id', help='Application ID')
	parser.add_argument('--password', help='Password')
	parser.add_argument('--language', help='Specifies recognition language of the document.')
	parser.add_argument('--textType', help='Specifies the type of the text on a page.')
	parser.add_argument('--exportFormat', help='Specifies the export format.')
	parser.add_argument('--pdfPassword', help='Contains a password for accessing password-protected images in PDF format.')
	args = parser.parse_args()


	application_id = "MGRC Document Management System"

	password = "lcPzjTiIo/Qb8bcMN0JcDo/C"

	ocr_engine = CloudOCR(application_id, password)
	parameters = {"region":"869,375,979,416","language":"English","letterSet":"","regExp":"","textType":"typewriter","oneTextLine":"false", "markingType": "simpleText"}
	parameters = {"region":"2136,268,2314,313","language":"English","letterSet":"","regExp":"","textType":"typewriter","oneTextLine":"false", "markingType": "simpleText"}
    
		
	input_file = open("E:\D\santa clara\classes\capstone\DOH Registration Card.pdf", 'rb')
	post_file = {input_file.name: input_file}
	result = ocr_engine.process_and_download(post_file, **parameters)
	for format, content in result.items():
		output_filename = 'abc5.xml'.format(name='.'.join(input_file.name.split('.')[:-1]), extension=format)
		with open(output_filename, 'wb') as output_file:
			output_file.write(content.read())
			output_file.close()