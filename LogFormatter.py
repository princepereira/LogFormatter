import json
import sublime
import os
import sublime_plugin
import sys

conf_file = "/.config/sublime-text-3/Packages/LogFormatter/preferences.json"
pip_path_file = "/.config/sublime-text-3/Packages/LogFormatter/pip-path.txt"
out_file = "/tmp/output.log"
input_file = "/tmp/input.log"


def get_pip_path():
	homedir = os.environ['HOME']
	fname = open(homedir + pip_path_file, 'r')
	path = fname.read()
	fname.close()
	return path.split("\n")[0]

site_path = get_pip_path()

if site_path not in sys.path:
	sys.path.append(site_path)

from texttable import Texttable

def fetch_remote_logs(remote_path):
	import pysftp
	with pysftp.Connection(host=remote_path["ip"], username=remote_path["username"], password=remote_path["password"]) as sftp:
		print("Connection succesfully established to : ",str(remote_path))
		sftp.get(remote_path["filepath"], input_file)
		print("File copied from remote location...")
		return

	print("Connection failed to : ",str(remote_path))

class RunCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		print("Running...............")
		homedir = os.environ['HOME']
		# Reading the json config
		with open(homedir + conf_file) as json_file:
			data = json.load(json_file)

		# Helper keys starts
		starts_with = data["Starts-with"]["input"].lower()
		excludes = data["Exclude-search"]["input"].lower().split(",")
		includes = data["Only-with-pattern"]["input"].lower().split(",")
		starts_with_set = False

		if starts_with != None and starts_with.strip() != "":
			starts_with_set = True

		# Helper keys ends

		try:
			if data["Load-logs-from"]["input"] == "window":
				contents = self.view.substr(sublime.Region(0, self.view.size()))
			else:
				fetch_remote_logs(data["Remote-path"])
				with open(input_file, 'r') as f:
					contents = f.read()

			if contents == None or len(contents) == 0:
				print("Unable to retrieve data...")
				return
				
		except Exception as exc:
			print("Exception happened while loading.. Exc : ", exc)
			return

		content_lines = contents.split("\n")
		headers = data["Valid-headers"]["input"]
		headers.append("value")

		t = Texttable()
		col_align = []
		col_width = []
		for key in headers:
			col_align.append('m')
			if key == "value":
				col_width.append(100)
			else:
				col_width.append(20)
		t.set_cols_align(col_align)
		t.set_cols_width(col_width)
		t.add_row(headers)

		for line in content_lines:

			if starts_with_set and starts_with not in line.lower():
				continue
			else:
				starts_with_set = False;

			comeout = False;

			for pat in excludes:
				pat = pat.strip()
				if pat != "" and pat in line.lower():
					comeout = True;
					break;
	            
			# Checking strict pattern
			if len(includes) > 0:
				for pat in includes:
					# print("Includes >>>>",pat, " line >> ",line)
					pat = pat.strip()
					if pat != "" and pat not in line.lower():
						# print("comeout...")
						comeout = True;
						break;

			if comeout:
				continue;
 
			try:
				json_row = json.loads(line)
				row = []
				for key in headers:
					try:
						row.append(str(json_row[key.rstrip()]))
					except:
						row.append("")
				t.add_row(row)

			except Exception as ex:
				pass

		with open(out_file, 'w') as f:
			f.write(t.draw())
		#print(t.draw())
		window = self.view.window()
		window.open_file(out_file)

class ConfigCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		#items = ['Text', 'Another']
		#self.view.show_popup_menu(items, self.on_done)
		homedir = os.environ['HOME']
		fname = open(homedir + conf_file, 'r')
		contents = fname.read()
		fname.close()
		window = self.view.window()
		window.show_input_panel("Edit config: ", contents, self.on_done, None, None)

	def invalid(self, json_res):

		try:

			if json_res["Load-logs-from"]["input"] not in ["window","remote"]:
				print("'Load-logs-from' field don't have the valid value. Expected : 'window/remote', Received : '", json_res["Load-logs-from"]["input"], "'")
				return True
			if json_res["Load-logs-from"]["input"] == "remote":
				if json_res["Remote-path"]["ip"] == "":
					print("'Load-logs-from' selected is 'remote'. But invalid ip. Received values : '", json_res["Remote-path"]["ip"], "'")
					return True
				if json_res["Remote-path"]["username"] == "":
					print("'Load-logs-from' selected is 'remote'. But invalid username. Received values : '", json_res["Remote-path"]["username"], "'")
					return True
				if json_res["Remote-path"]["password"] == "":
					print("'Load-logs-from' selected is 'remote'. But invalid password. Received values : '", json_res["Remote-path"]["password"], "'")
					return True
				if json_res["Remote-path"]["filepath"] == "":
					print("'Load-logs-from' selected is 'remote'. But invalid filepath. Received values : '", json_res["Remote-path"]["filepath"], "'")
					return True
		except Exception as ex:
			print("Failed at json validity check. Ex : ", ex)
			return True

		return False

	def on_done(self, result):
		try:
			json_res = json.loads(result)

			if self.invalid(json_res):
				return
			
			homedir = os.environ['HOME']

			# Reading the json config
			with open(homedir + conf_file) as json_file:
				data = json.load(json_file)
				data["Load-logs-from"]["input"] = json_res["Load-logs-from"]["input"]
				data["Remote-path"]["ip"] = json_res["Remote-path"]["ip"]
				data["Remote-path"]["username"] = json_res["Remote-path"]["username"]
				data["Remote-path"]["password"] = json_res["Remote-path"]["password"]
				data["Remote-path"]["filepath"] = json_res["Remote-path"]["filepath"]
				data["Starts-with"]["input"] = json_res["Starts-with"]["input"]
				data["Only-with-pattern"]["input"] = json_res["Only-with-pattern"]["input"]
				data["Exclude-search"]["input"] = json_res["Exclude-search"]["input"]
				data["Valid-headers"]["input"] = json_res["Valid-headers"]["input"]

			# Storing the updated json config
			with open(homedir + conf_file, 'w') as f:
				json.dump(data, f, indent=4)

		except Exception as ex:
			print("An exception occurred ",ex)

