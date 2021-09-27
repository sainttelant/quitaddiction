from subprocess import check_output, STDOUT, CalledProcessError
from typing import Set
import os
class VideoProcess:
    def __init__(self,filename,key_encript,key_decript):
        self.filename = filename
        self.encryptionname_suffix = self.filename.split(".")[1]
        if not "_encrypt" in self.filename:
            self.encryptionname = self.filename.split(".")[0]+"_encrypt"+"."+self.encryptionname_suffix
        else:
            self.encryptionname = self.filename.split(".")[0].replace("_encrypt","")+"." + self.encryptionname_suffix
        self.key_encript = ""
        self.key_decript = ""
        self.schema_encript = "cenc-aes-ctr"
        self.key_encript = key_encript
        self.key_decript = key_decript

    def SetCommand(self):
        
        ffmpeg_command = ['ffmpeg', 
            '-i', self.filename, 
            "-vcodec", "copy",
            "-encryption_scheme", self.schema_encript, 
            "-encryption_key", self.key_encript,
            "-encryption_kid", self.key_decript, self.encryptionname]

        return ffmpeg_command

    def SetdecriptCommand(self):
        ffmpeg_command = ['ffmpeg', 
            "-decryption_key", self.key_encript,
            '-i', self.filename, 
            '-vcodec', 'copy', self.encryptionname]
        return ffmpeg_command

    def startdecrytion(self):
        
        decript_command= self.SetdecriptCommand()
        try:
            output_ffmpeg_execution = check_output(decript_command, stderr=STDOUT)
            print(output_ffmpeg_execution)
        except CalledProcessError as e:
            print(e)
            print(e.output)



    def startencrytion(self):
        ffmpeg_commands = self.SetCommand()    
        try:
            output_ffmpeg_execution = check_output(ffmpeg_commands, stderr=STDOUT)
            print(output_ffmpeg_execution)
        except CalledProcessError as e:
            print(e)
            print(e.output)
        os.remove(self.filename)
   