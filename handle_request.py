import json
import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from widgets import LoadingPopup

class RequestHandler:

	development = True
	url_link = "https://test888.netlify.app"
	dev_link = "http://localhost:8888"

	widget = None
	loading = None

	@staticmethod
	def get_link():
		if RequestHandler.development:
			return RequestHandler.dev_link
		return RequestHandler.url_link

	@staticmethod
	def request_loader(target):
		current_running = App.get_running_app()
		screen = current_running.sm.get_screen(current_running.sm.current)

		if not RequestHandler.widget:
			RequestHandler.widget = screen

		if not RequestHandler.loading:
			RequestHandler.loading = LoadingPopup()

		screen.add_widget(RequestHandler.loading)
		threading.Thread(target=target).start()

	@staticmethod
	def create_req_suc_error(method, link, data={}, on_success=None, on_error=None):
		result, response = RequestHandler.create_request(
			method=method,
			link=link,
			data=data
		)
		if result:
			if on_success:
				RequestHandler.on_success(on_success, response)
		else:
			if on_error:
				RequestHandler.on_error(on_error, response)

	def on_success(on_success, result):
		Clock.schedule_once(lambda _: RequestHandler.run_and_remove(on_success, result))

	def on_error(on_error, error):
		Clock.schedule_once(lambda _: RequestHandler.run_and_remove(on_error, error))

	def run_and_remove(function, result):
		function(result)
		RequestHandler.widget.remove_widget(RequestHandler.loading)
		RequestHandler.widget = None

	@staticmethod
	def create_request(method, link, data={}):
		try:
			req = None
			if method == "post":
				req = requests.post
			elif method == "get":
				req = requests.get
			elif method == "put":
				req = requests.put
			elif method == "delete":
				req = requests.delete

			response = req(
				f'{RequestHandler.get_link()}/.netlify/functions/api/{link}',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()
			result = response.json()
			return result.get('success'), result

		except requests.RequestException as e:
			if e.response is not None:
				try:
					error_message = e.response.json().get('message', str(e) if not RequestHandler.development else "Connection Error. Login Failed.")
				except json.JSONDecodeError:
					error_message = e.response.text
			else:
				error_message = str(e) if not RequestHandler.development else "Connection Error. Login Failed."
			return False, { 'message': error_message }

