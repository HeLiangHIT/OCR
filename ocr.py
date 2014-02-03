#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image,tesseract,sys
from pytesser import *
#import cv2.cv as cv

def tesseract_ocr(imgname,type='PagesWrapper'):
	api = tesseract.TessBaseAPI()
	api.SetOutputName("outputName");
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)
	if type=='PagesWrapper':
		result = tesseract.ProcessPagesWrapper(imgname,api)
	elif type=='PagesFileStream':
		result = tesseract.ProcessPagesFileStream(mImgFile,api)
	elif type=='PagesRaw':
		result = tesseract.ProcessPagesRaw(mImgFile,api)
	elif type=='PagesBuffer':
		mBuffer=open(imgname).read()
		result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
	return result

def tesseract_cv_ocr(imgname):
	image=cv.LoadImage(imgname)
	api = tesseract.TessBaseAPI()
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	#api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
	api.SetPageSegMode(tesseract.PSM_AUTO)
	tesseract.SetCvImage(image,api)
	text=api.GetUTF8Text()
	conf=api.MeanTextConf()
	return text
	#print conf

def pytesser_ocr(imgname,ft='.png'):
	if ft=='.tif':
		im = Image.open(imgname)
		text = image_to_string(im)
	else:
		text = image_file_to_string(imgname, graceful_errors=True)
	return text

def init_im_to_string(imgname):
	im=Image.open(imgname)
	im=im.convert('L')
	#im=im.convert('1')
	im.show()
	text = image_to_string(im)
	return text

def usage():
	print '='*80
	print 'Usage:'
	print '     %s [-p | -t | -tt type | -i] ImageName' % sys.argv[0]
	print '     -p : use pytesser'
	print '     -t : use tesseract (default)'
	print '     -tt : use tesseract and set the type'
	print '     -i : pretreatment of image before recognition'
	print '     type: PagesWrapper | PagesFileStream | PagesRaw | PagesBuffer'
	print 'eg:'
	print '     %s 1.png' % sys.argv[0]
	print '     %s -p 1.png' % sys.argv[0]
	print '     %s -tt PagesWrapper 1.png' % sys.argv[0]
	print '='*80

if __name__=='__main__':
	if len(sys.argv)<2:
		usage()
	else:
		if sys.argv[-1][-4:]=='.tif':
			print pytesser_ocr(sys.argv[-1],'.tif')
		elif sys.argv[1]=='-p':
			print pytesser_ocr(sys.argv[-1])
		elif sys.argv[1]=='-tt':
			print tesseract_ocr(sys.argv[-1],sys.argv[-2])
		elif sys.argv[1]=='-i':
			print init_im_to_string(sys.argv[-1])
		else:
			print tesseract_ocr(sys.argv[-1])