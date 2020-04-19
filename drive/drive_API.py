from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

mimetype_types = {'text':'text/plain',
                  'imgjpeg':'image/jpeg',
                  'imgpng':'image/png',
                  'pdf':'application/pdf',
                  'doc':'application/vnd.oasis.opendocument.text'}

# If modifying these scopes, delete the file token.pickle.
SCOPES = 'https://www.googleapis.com/auth/drive'

def listFiles(service):
	results = service.files().list(
	pageSize=10, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	if not items:
		print('No files found.')
	else:
		print('Files:')
		for item in items:
			print(u'{0} ({1})'.format(item['name'], item['id']))

def UploadFile(service,file_name,file_type):
	file_metadata = {'name': file_name}
	media = MediaFileUpload(file_name,
	                        mimetype = file_type)
	file = service.files().create(body=file_metadata, 		
	                              media_body=media,
	                              fields='id').execute()
	print('File ID: '+str(file.get('id')))

def DownloadFile(service,file_id,path):
	request = service.files().get_media(fileId = file_id)
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh,request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
		print('Download '+str(int(status.progress()*100))+'%%.')
	with open(path,'wb') as f:
		fh.seek(0)
		f.write(fh.read())

def DownloadDoc(service,file_id,file_type,path):
	request = service.files().export_media(fileId = file_id, mimeType=file_type)
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh,request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
		print('Download '+str(int(status.progress()*100))+'%%.')
	with open(path,'wb') as f:
		fh.seek(0)
		f.write(fh.read())

def main():
	"""Shows basic usage of the Drive v3 API.
	Prints the names and ids of the first 10 files the user has access to.
	"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('drive', 'v3', credentials=creds)

	# Call the Drive v3 API
	
	#listFiles(service)
	#UploadFile(service,'document.pdf',mimetype_types['pdf'])
	#DownloadFile(service,'FILEID','path')
	#DownloadDoc(service,'FILEID',mimetype_types['pdf'],'document.pdf')
	
if __name__ == '__main__':
	main()
