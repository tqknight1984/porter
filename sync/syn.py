##coding=utf-8
import paramiko
import os
import sys
from stat import S_ISDIR
import ConfigParser
import hashlib
import json
import fnmatch
import time
import sqlite3

def callback(size, file_size):
    if (file_size > 0):
        prec = int(1.0 * size/file_size * 100)

def generate_file_md5(fpath):
    m = hashlib.md5()
    a_file = open(fpath, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

def getfile(remote_path,recvfiles,sftp):
    for k in recvfiles.split(','):
        fname = os.path.basename(k)
        r_path = remote_path + '/' + fname      
        print r_path  
        sftp.get(r_path,"./" + fname)


class Config:
    
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
        print self.path
    def sections(self):
        return self.cf.sections()
    def get(self, field, key):
        result = ""
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result
    def set(self, filed, key, value):
        try:
            self.cf.set(field, key, value)
            cf.write(open(self.path,'w'))
        except:
            return False
        return True

class Syn:
    def __init__(self, path, section):
        self.cfg = Config(path)
        self.section = section
    
    def connect_server(self,ip,port,user,passwd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh = paramiko.Transport((ip, int(port)))
        #ssh.connect(username=user, password=passwd)
        ssh.connect(ip,int(port),user, passwd)
        self.ssh = ssh
        self.sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())


    def exist(self,sftp,remote_path):
        try:
            return S_ISDIR(sftp.lstat(remote_path).st_mode) 
        except IOError:
            return False

    def r_mkdir(self,sftp,remote_path):
        try:
            return sftp.mkdir(remote_path)
        except:
            return False
    def r_mkdirs(self,sftp,remote_path):
        r = remote_path.split('/')
        for i in range(2,len(r) + 1):
            if self.exist(sftp,'/'.join(r[0:i])) == False:
                self.r_mkdir(sftp,'/'.join(r[0:i]))
    #{remote : local}    
    def sendfiles(self,sftp,sendfiles):
        for k,v in sendfiles.items():
            k = k.replace('\\', "/")
            if self.exist(sftp,os.path.dirname(k)) == False:
                self.r_mkdirs(sftp,os.path.dirname(k))
            print u'%s---->%s' % (v, k)
            sftp.put(v,k,callback=callback)
            # sftp.put(v, os.path.join(k, fname))

    def postCmd(self,section):
        cmd = self.cfg.get(section,'post_cmd')
        self.runCmd(section,cmd)
    def prevCmd(self,section):
        cmd = self.cfg.get(section,'prev_cmd')
        self.runCmd(section,cmd)

    def runCmd(self,section,cmd):
        if (cmd <> None and len(cmd) > 0):
            tc_cmd = cmd.split(";")
            chan = self.ssh #.open_session()
            for m in tc_cmd:
                stdin, stdout, stderr = chan.exec_command(m)
                print m
                for line in stderr:
                    print line.strip('\n') 
                for line in stdout:  
                    print ' ' * 2 + line.strip('\n') 
            print 'OK'


    def updateAll(self,proj_path):
        if (self.section == 'all'):
            for section in self.cfg.sections():
                self.update(proj_path,section)
        else:
            self.update(proj_path,self.section)

    def update(self,proj_path,section):
        ip = self.cfg.get(section,'ip')
        port = self.cfg.get(section,'port')
        user = self.cfg.get(section,'user')
        pswd = self.cfg.get(section,'pass')
        tmp = self.cfg.get(section,'exclude').strip()
        if (tmp == ''):
            excludes = None
        else:
            excludes = tmp.split(",")

        tmp = self.cfg.get(section,'include').strip()
        if (tmp == ''):
            includes = None
        else:        
            includes = tmp.split(",")

        print includes,excludes
        self.connect_server(ip,port,user,pswd)
        old_t = time.time()
        self.prevCmd(section)
        print "prev cmd time:",time.time() - old_t
        #
        r_path = self.cfg.get(section,'remote_path')
        #create root path
        self.r_mkdirs(self.sftp,r_path)

        #加载原来上传记录
        old_md5 = {}
        sql = sqlite3.connect(proj_path + '/.syn.db')
        sql.execute('create table if not exists obj_sftp(id INTEGER primary key autoincrement not null,f_cat text,f_path text,f_md5 text)')
        sql.commit()
        sql_cur = sql.cursor()
        sql_cur.execute("select f_path,f_md5 from obj_sftp where f_cat = '" + section + "'")
        res = sql_cur.fetchall()
        for r in res:
            old_md5[r[0]] = r[1]
        sql_cur.close()

        # log_path = proj_path + '/.syn_' + section        
        # try:
        #     if (os.path.exists(log_path) == True):
        #         with open(log_path) as json_file:
        #             old_md5 = json.load(json_file)
        # except:
        #     pass

        new_md5 = {}
        list_files = {}
        old_t = time.time()
        l_path = self.cfg.get(section,'local_path')
        for root,dirs,files in os.walk(l_path):
            for d in dirs:
                temp = r_path + os.path.join(root,d).replace(l_path,'')
                self.r_mkdirs(self.sftp,temp)
            for f in files:
                local_path = os.path.join(root,f)
                remote_path = r_path + os.path.join(root,f).replace(l_path,'')
                flag = False
                if (includes == None):
                    flag = True
                else:
                    for pat in includes:
                        if (fnmatch.fnmatch(local_path,pat) == True):
                            flag = True
                            break
                if (flag == True and excludes <> None):
                    for pat in excludes:
                        if (fnmatch.fnmatch(local_path,pat) == True):
                            flag = False
                            break
                if (flag == True):                         
                    m5 = generate_file_md5(local_path)
                    new_md5[local_path] = m5
                    flag = old_md5.get(local_path,None)
                    if (flag <> m5):
                        list_files[remote_path] = local_path
        new_t = time.time()
        print "md5 time:",new_t - old_t
        self.sendfiles(self.sftp,list_files)

        sql.execute("delete from obj_sftp where f_cat = '" + section + "'")
        for k,v in new_md5.items():
            sql.execute("insert into obj_sftp(f_cat,f_path,f_md5) values('%s','%s','%s')" %(section,k,v))
        sql.commit()
        sql.close()
        self.postCmd(section)
        print "post cmd time:",time.time() - new_t
        # with open(log_path, 'w') as json_file:
        #     json_file.write(json.dumps(new_md5))
        

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print 'usage: python syn.py [update/clean] session'
        exit(1)
    proj_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    handler = Syn(proj_path + "/syn.conf",sys.argv[2])
    if (sys.argv[1] == "update"):
        handler.updateAll(proj_path)
    elif (sys.argv[1] == "clean"):
        init_session(cfg)
