# SAMP functions for SharpCap
# Version 1.2 2024-03-12 GUI
# Version 1.1 2024-01-21 control mount from Aladin
# Version 1.0 2024-01-17 initial version 
# Author: renaud.savalle@obspm.fr

import time
# Mount control: use SharpCap exposed classes
from SharpCap.Base import RADecPosition, Epoch

# GUI: use .NET classes
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import *
from System.Drawing import *

# Icon for SAMP button
padc_icon="C:\\Users\\User\\Documents\\SAMP\\PADC.ico"


def samp_init():
	"""
	init SharpCap for using SAMP. Customize for your system
	"""
	# Import SharpNum
	import clr
	clr.AddReferenceToFileAndPath('C:\\USERS\\USER\\Lib\\NumSharp.0.20.5\\NumSharp.Core.dll')
	import NumSharp.np as np 

	# Change sys.path to use astropy.samp
	import sys
	#sys.path=['', 'C:\\USERS\\USER\\.conda\\envs\\sharpcap-py3.4\\python34.zip', 'C:\\USERS\\USER\\.conda\\envs\\sharpcap-py3.4\\DLLs', 'C:\\USERS\\USER\\.conda\\envs\\sharpcap-py3.4\\lib', 'C:\\USERS\\USER\\.conda\\envs\\sharpcap-py3.4', 'C:\\USERS\\USER\\.conda\\envs\\sharpcap-py3.4\\lib\\site-packages', 'C:\\USERS\\USER\\.conda\\envs\\sharpcap-py3.4\\lib\\site-packages\\setuptools-27.2.0-py3.4.egg']
	sys.path.append('C:\\PROGRAMDATA\MINICONDA3\\envs\\sharpcap-py3.4\\lib\\site-packages')
	
	import astropy.samp



def function_samp_receive_notification_pointat(private_key, sender_id, mtype, params, extra):
	"""
	Called when a SAMP mtype coord.pointAt.sky is received
    FOR TESTING
	"""
	
	print("*** [func] Received Notification mtype="+mtype)
	
	# retrieve coordinates sent
	try:
		ra = float(params['ra'])/15.0
		dec = float(params['dec'])
		print(f"*** [func] Received coordinates ra={ra:.6f} dec={dec:.6f}")
	except Exception as e:
		print('ERROR: '+str(e))
	
	else:	
		try:
			function_slew_mount(ra, dec)
		except Exception as e:
			print('ERROR: '+str(e))
			

class Receiver(object):
	"""
	Receiver class: receive SAMP notification and messages
	"""


	def __init__(self, client, parent=None):
		self.client = client
		self.received = False
		self.parent = parent
		print('Receiver init parent='+str(parent))
		
	
	def log_info(self, text):
		if self.parent!=None:
			self.parent.log_info(text)
		else:
			print(text)
	
	def log_error(self, text):
		if self.parent!=None:
			self.parent.log_error(text)
		else:
			print('ERROR: '+text)
		
        
	#def receive_call(self, private_key, sender_id, msg_id, mtype, params, extra):
	#	print('receive_call', params)
	#	self.params = params
	#	self.received = True
	#	self.client.reply(msg_id, {"samp.status": "samp.ok", "samp.result": {}})
    
	def receive_notification(self, private_key, sender_id, mtype, params, extra):

		# try to get sender name
		sender_name = sender_id # by default we only know the id (ex: "c1")
		try:
			metadata = self.client.get_metadata(sender_id)
			sender_name = metadata["samp.name"]
		except Exception as e:
			self.log_error(str(e))

		self.log_info('Received notification mtype='+mtype+' from '+sender_name) # +' params='+str(params))
		
		#self.params = params
		#self.received = True
        
		if mtype == 'coord.pointAt.sky':
        	
			# retrieve coordinates sent
			try:
				ra = float(params['ra'])
				dec = float(params['dec'])
				self.log_info(f"Received coordinates ra={ra:.6f} dec={dec:.6f}")
			except Exception as e:
				self.log_error('ERROR: '+str(e))
		
			else:
				# Slew mount to coordinates
				try:
					# parent class is MySampClient, parent.parent class is SAMPForm
					self.parent.parent.fromLabel.Text = 'Coordinates from '+str(sender_name)
					self.parent.parent.raTextBox.Text = str(ra)
					self.parent.parent.decTextBox.Text= str(dec)
					#self.parent.parent.slewMount(ra/15.0, dec)
				except Exception as e:
					self.log_error('ERROR: '+str(e))
			
		else:
			self.log_info('mtype'+str(mtype)+' not implemented')
			
        
class MySampClient:
	"""
	SAMP client
	"""
	client = None # astropy.samp.SAMPIntegratedClient - manage communication with SAMP hub
	receiver = None # Receiver - manage notifications
	name = None # name to be shown in SAMP hub
	parent = None # if running in GUI mode, this points to SAMPForm object


	def log_info(self, text):
		#print('log_info parent='+str(self.parent))
		if self.parent!=None:
			self.parent.log_info(text)
		else:
			print(text)
	
	
	def log_error(self, text):
		if self.parent!=None:
			self.parent.log_error(text)
		else:
			print('ERROR: '+text)

	def __init__(self, name='SharpCap', parent=None):
		"""
        create SAMP client and init receiver
		"""
	
		from astropy.samp import SAMPIntegratedClient
		
		self.name = name
		self.client = SAMPIntegratedClient(name)
		self.parent = parent
		
		self.receiver = Receiver(self.client, self)
		


	def connect(self):
		"""
		Connect to SAMP hub and setup notification bindings
		"""
    
		self.log_info('Connecting to SAMP hub...')
		try: 
			self.client.connect()
			#log_info(self.client.get_private_key())
		except Exception as e:
			self.log_error(str(e))
		else:
			self.log_info('Connected.')

			# Bind notifications for mtypes
			mtype="coord.pointAt.sky"

			try:
				if self.parent == None: # CLI, use function
					self.log_info('Binding notification for mtype='+mtype+' to func function_samp_receive_notification_pointat')
					self.client.bind_receive_notification(mtype, function_samp_receive_notification_pointat)
				else: # GUI, use method
					self.log_info('Binding notification for mtype='+mtype+' to method self.receiver.receive_notification')
					self.client.bind_receive_notification(mtype, self.receiver.receive_notification)
			except Exception as e:
				self.log_error(str(e))
			else:
				self.log_info('Binding OK')
			
	def disconnect(self):
		"""
		Disconnect from SAMP hub
		"""
		self.log_info('Disconnecting...')
		try:
			self.client.disconnect()
		except Exception as e:
			self.log_error(str(e))

#	def send_fits(self, url, name=None):
#		"""
#		Send an image to all SAMP clients
#		Example: 
#		"""
#	
#		if name is None:
#			name = f'from {self.name}'
#	
#		params = {}	
#		params["url"] = url
#		params["name"] = name
#		message = {}
#		message["samp.mtype"] = "image.load.fits"
#		message["samp.params"] = params
#		self.client.notify_all(message)



#	def get_coords(self,recipient_id):
#		"""
#		Example: c.get_coords('c1') # retrieve coordinates from another SAMP client 
#		"""
#		ra = None
#		dec = None
#	
#		params = {}
#		message = {}
#		message["samp.mtype"] = "coord.get.sky"
#		message["samp.params"] = params
#		timeout="10"
#		
#		response = self.client.call_and_wait(recipient_id, message, timeout)
#		status = response['samp.status']
#		if status == 'samp.ok':
#			result = response['samp.result']
#			ra = result['ra']
#			dec = result['dec']
#			self.log_info(f'Received ra={ra} dec={dec}')
#		else:
#			self.log_info(f'ERROR: samp.status is not samp.ok but: {status}')
#		
#		return ra, dec
		

#	def receive(self, mtype='image.load.fits'):
#		"""
#		Example: c.receive()
#		"""
#		r = Receiver(self.client)
#		
#		
#		self.client.bind_receive_call(mtype, r.receive_call)
#		self.client.bind_receive_notification(mtype, r.receive_notification)
#		
#		import time
#		while r.received==False:
#			time.sleep(1)
#		return r.params



	
def function_slew_mount(ra, dec):
	"""
	Slew mount
	FOR TESTING
	"""

	print(f"Slewing mount to RA={ra} h Dec={dec} deg")
	radp = RADecPosition(ra, dec, Epoch.J2000)
	SharpCap.Mounts.Current.SlewTo(radp)
	print(f"Slew in progress")
	
# GUI

# Inspired from Jean-Francois (cf https://forums.sharpcap.co.uk/viewtopic.php?p=40497)
#
class StatePanel(Panel):
    """
    Control panel with log window
    """
    def __init__(self, label, width, height):
        super(StatePanel, self).__init__()
        self.Width = width
        self.Height = height
        label_widget = Label()
        label_widget.Text = label
        label_widget.Dock = DockStyle.Top
        label_widget.Height = 25
        label_widget.BackColor = Color.LightGray
        label_widget.Font = Font(label_widget.Font, FontStyle.Bold)
        label_widget.Padding = Padding(3)

        state_widget = RichTextBox()
        state_widget.Dock = DockStyle.Top
        state_widget.Height = height - label_widget.Height
        state_widget.Multiline = True
        state_widget.ScrollBars = RichTextBoxScrollBars.Vertical
        state_widget.WordWrap = True
        state_widget.ReadOnly = True

        self.Controls.Add(state_widget)
        self.Controls.Add(label_widget)
        self.label = label_widget
        self.info = state_widget

    def log(self, text, error=False):
        start_selection = self.info.Text.Length
        self.info.ReadOnly = False
        self.info.AppendText(str(text)+"\n")
        self.info.ReadOnly = True
        if error:
            self.info.SelectionStart = start_selection
            self.info.SelectionLength = self.info.Text.Length - start_selection
            self.info.SelectionColor = Color.Red
        self.info.SelectionStart = self.info.Text.Length
        self.info.ScrollToCaret()

    def log_status(self, text):
        self.label.Text = (str(text))

    def log_error(self, text):
        self.log(text, True)
        
    def log_info(self, text):
        self.log(text, False)
        
    def clear_log(self):
        self.info.ReadOnly = False
        self.info.Text = ""
        self.info.ReadOnly = True
        
        
class SAMPForm(Form):
	"""
	SAMP Control Panel form
	"""

	def __init__(self):
		self.Text = "SAMP Control Panel"
		#self.Width=1000
		#self.Height=500
		self.setup()

	def setup(self):

		# define log panel
		self.logPanel = StatePanel("Log", width=528, height=237)
		self.logPanel.Location = Point(206,12)
		self.logPanel.BackColor = Color.White
		self.logPanel.BorderStyle = BorderStyle.FixedSingle

		# logPanel
		#
		#self.logPanel.Controls.Add(self.logVScrollBar)
		#self.logPanel.Controls.Add(self.logHScrollBar)

		# add log panel
		#self.Controls.Add(self.logPanel)


		self.fromLabel = Label()
		self.logHScrollBar = HScrollBar()
		self.logVScrollBar = VScrollBar()
		self.raTextBox = TextBox()
		self.raLabel = Label()
		self.decLabel = Label()
		self.decTextBox = TextBox()
		self.slewButton = Button()

		#self.logPanel.SuspendLayout()
		#self.SuspendLayout()

		#
		# fromLabel
		#
		self.fromLabel.Location = Point(13, 13)
		self.fromLabel.Name = "label_from"
		self.fromLabel.Size = Size(200, 23)
		#self.fromLabel.Text = "Coordinates from"
		#self.label_from.Click += self.Label1Click
		#

		#
		# raLabel
		#
		self.raLabel.Location = Point(16, 42)
		self.raLabel.Name = "raLabel"
		self.raLabel.Size = Size(50, 23)
		self.raLabel.Text = "RA (J2000)"
		#self.raLabel.Click += self.raLabelClick
		#
		# raTextBox
		#
		self.raTextBox.Location = Point(87, 39)
		self.raTextBox.Name = "raTextBox"
		self.raTextBox.Size = Size(100, 20)
		#
		# decLabel
		#
		self.decLabel.Location = Point(16, 65)
		self.decLabel.Name = "decLabel"
		self.decLabel.Size = Size(50, 23)
		self.decLabel.Text = "Dec (J2000)"
		#self._decLabel.Click += self.decLabelClick
		#
		# decTextBox
		#
		self.decTextBox.Location = Point(87, 62)
		self.decTextBox.Name = "decTextBox"
		self.decTextBox.Size = Size(100, 20)
		#self.decTextBox.TextChanged += self.decTextChanged
		#
		# slewButton
		#
		self.slewButton.Location = Point(52, 92)
		self.slewButton.Name = "slewButton"
		self.slewButton.Size = Size(108, 23)
		self.slewButton.TabIndex = 6
		self.slewButton.Text = "Slew"
		self.slewButton.UseVisualStyleBackColor = True
		self.slewButton.Click += self.slewButtonClick
		#
		# MainForm
		#
		self.ClientSize = Size(746, 261)

		self.Controls.Add(self.slewButton)
		self.Controls.Add(self.decLabel)
		self.Controls.Add(self.decTextBox)
		self.Controls.Add(self.raLabel)
		self.Controls.Add(self.raTextBox)
		self.Controls.Add(self.logPanel)
		self.Controls.Add(self.fromLabel)
		#self.Name = "MainForm"
		#self.Text = "Wivona"
		#self.logPanel.ResumeLayout(False)
		#self.ResumeLayout(False)
		self.PerformLayout()

	def slewButtonClick(self, sender, e):
		# Slew mount to coordinates
		try:
			# retrieve coordinates from text boxes
			ra = float(self.raTextBox.Text)
			dec = float(self.decTextBox.Text)

			# slew mount, expect RA coordinates in Hours
			self.slewMount(ra/15.0, dec)
		except Exception as e:
			self.log_error('ERROR: ' + str(e))
		pass

	def log_info(self, text):
		self.logPanel.log_info(time.strftime("%H:%M:%S") + ": " + text)

	def log_error(self, text):
		self.logPanel.log_error(time.strftime("%H:%M:%S") + ": " + text)

	def slewMount(self, ra, dec):
		"""
		Slew mount with confirmation dialog
		"""
		#self.log_info(f"=== [method] Request to slew mount to ra={ra:.6f} dec={dec:.6f}")

		current_mount = SharpCap.Mounts.Current
		if current_mount.IsAvailable:


			#self.log_info("DIALOG")
			#confirm = MessageBox.Show(f"Do you want to slew the mount to RA={ra:.6f} DEC={dec:.6f} ?","Confirm",MessageBoxButtons.YesNo)
			confirm = MessageBox.Show(Form.ActiveForm,f"Slew the mount to RA={ra:.6f} h DEC={dec:.6f} deg ?","Confirm Slew",MessageBoxButtons.YesNo)

			#self.log_info(str(confirm))

			if str(confirm) == 'Yes':
				try:
					radp = RADecPosition(ra, dec, Epoch.J2000) # Aladin coordinates sent in J2000
					current_mount.SlewTo(radp)
				except Exception as e:
					self.log_error(str(e))
				else:
					self.log_info(f"Slew in progress")

		else:
			self.log_info("Mount is not available")

		
	def startSAMP(self):
		# Create client, attach to this form
		self.samp_client = MySampClient(parent=self)
		# Connect to HUB
		self.samp_client.connect()


	def OnClosed(self, e):
		"""
		Called when the SAMP control form is closed
		"""
		try:
			#confirm = MessageBox.Show(Form.ActiveForm, f"Disconnect from SAMP ?",
			#						  "Confirm Disconnect", MessageBoxButtons.YesNo)

			self.samp_client.disconnect()
		except:
			self.log_error(str(e))
		Form.OnClosed(self, e)


def create_form():
	#print("create_form")
	form = SAMPForm()
	#print(padc_icon)
	#form.icon = Icon(padc_icon)
	form.StartPosition = FormStartPosition.CenterScreen
	form.TopMost=False # True => windows always on top
	form.Show()
	form.log_info("Form ready")
	#form.log_error("TEST ERROR")
	form.startSAMP()

	
	
	


# main 
print("Starting SAMP")
samp_init()
#c=MySampClient() # done in GUI
# init GUI
print("Creating GUI")
custom_button = SharpCap.AddCustomButton("SAMP", Image.FromFile(padc_icon), "SAMP", create_form)


	
	
		


