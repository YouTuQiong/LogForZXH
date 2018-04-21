import hashlib as Hash
class Encryption:
    defaultSalt = "GoodLand"
    def MD5Encryption(self,string):
        MD5 = Hash.md5()
        defaultSalt  = self.defaultSalt  + str(string)
        MD5.update(defaultSalt.encode("utf8"))
        return MD5.hexdigest()
    def SHA256Encryption(self,string):
        SHA = Hash.sha256()
        defaultSalt  = self.defaultSalt  + str(string)
        SHA.update(defaultSalt.encode("utf8"))
        return SHA.hexdigest()