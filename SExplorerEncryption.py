from os import chdir, mkdir, getcwd, listdir, remove
from os.path import isdir, isfile, join as pathjoin, dirname, basename

from hashlib import sha256
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet

class SEE:
	def __init__(self):
		self.password = None
		return
	
	def spin(self) -> None:
		runLoop = True
		path = None
		print("\"n\" or \"new password\" to set a new encryption/decryption password")
		print("\"e\" or \"encrypt\" to encrypt a file")
		print("\"d\" or \"decrypt\" to decrypt a file")
		print("\"s\" to set current path (can be file or dir)")
		print("\"exit\" to quit")
		while runLoop:
			opt = input(getcwd()+"$ ")
			if opt == "e" or opt == "encrypt":
				self.encrypt(path)
			elif opt == "d" or opt == "decrypt":
				self.decrypt(path)
			elif opt == "n" or opt.find("password") > 0:
				self.password = input("New Password: ").encode('utf8')
			elif opt == "s":
				path = input("Please enter path: ")
				try:
					if path[0] != "/":
						path = pathjoin(getcwd(), path)
				except IndexError:
					path = getcwd()
				finally:
					print(f"New path set to: {path}")
			elif opt == "exit":
				runLoop = False
			else:
				print("\"n\" or \"new password\" to set a new encryption/decryption password")
				print("\"e\" or \"encrypt\" to encrypt a file")
				print("\"d\" or \"decrypt\" to decrypt a file")
				print("\"s\" to set current path (can be file or dir)")
				print("\"exit\" to quit")
		return

	def encrypt(self, path : str = None):
		if not self.password:
			print("Unable to encrypt without password")
			return
		elif not path:
			print("No files or directories given to encrypt")
			return
		key = urlsafe_b64encode(sha256(self.password).digest())
		enc = Fernet(key)
		if isdir(path):
			for f in listdir(path):
				if isdir(pathjoin(path, f)):
					self.encrypt(pathjoin(path, f))
					continue
				with open(pathjoin(path, f), "r") as fd:
					data = fd.read()
				with open(pathjoin(path, f.replace(".","_")+".enc"), "wb") as fd:
					encryptedData = enc.encrypt(data.encode("utf8"))
					fd.write(encryptedData)
				remove(pathjoin(path, f))
		elif isfile(path):
			f = basename(path)
			path = dirname(path)
			with open(pathjoin(path, f), "r") as fd:
					data = fd.read()
			with open(pathjoin(path,f.replace(".","_")+".enc"), "wb") as fd:
				encryptedData = enc.encrypt(data.encode("utf8"))
				fd.write(encryptedData)
		else:
			print("Path does not exist. Unable to encrypt.")
		return
	
	def decrypt(self, path : str = None):
		if not self.password:
			print("Unable to decrypt without password")
			return
		elif not path:
			print("No files or directories given to decrypt")
			return
		key = urlsafe_b64encode(sha256(self.password).digest())
		enc = Fernet(key)
		if isdir(path):
			for f in listdir(path):
				if isdir(pathjoin(path, f)):
					self.decrypt(pathjoin(path, f))
					continue
				with open(pathjoin(path, f), "rb") as fd:
					data = fd.read()
				with open(pathjoin(path ,f.replace("_",".").removesuffix(".enc")), "w") as fd:
					decryptedData = enc.decrypt(data)
					fd.write(decryptedData.decode('utf8'))
				remove(pathjoin(path, f))
		elif isfile(path):
			f = basename(path)
			path = dirname(path)
			with open(pathjoin(path, f), "rb") as fd:
					data = fd.read()
			with open(pathjoin(path, f.replace("_",".").removesuffix(".enc")), "w") as fd:
				decryptedData = enc.decrypt(data)
				fd.write(decryptedData.decode("utf8"))
			remove(pathjoin(path, f))
		else:
			print("Path does not exist. Unable to encrypt.")
		return

def main():
	see = SEE()
	see.spin()
	return

if __name__ == "__main__":
	main()