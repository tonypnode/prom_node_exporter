from os import system as system, rename, chown, remove, path as os_path
from shutil import rmtree
from contextlib import closing
import grp
import pwd
import hashlib
import tarfile


# TODO I should prolly remove most of this data from the file and create a config file
username = 'node_exporter'
exporter_url = 'https://github.com/prometheus/node_exporter/releases/download/v0.16.0/'
exporter_file = 'node_exporter-0.16.0.linux-amd64.tar.gz'
exporter_sha = 'e92a601a5ef4f77cce967266b488a978711dabc527a720bea26505cba426c029'
exporter_working_dir = './node_exporter-0.16.0.linux-amd64'
bin_file_name = 'node_exporter'
bin_file_dest = '/usr/local/bin'
svc_name = 'node_exporter'
svc_location = '/etc/systemd/system/'
svc_file_extention = '.service'
svc_definition = ''' [Unit]\n 
Description=Node Exporter\n
Wants=network-online.target\n
After=network-online.target\n
\n
[Service]\n
User=node_exporter\n
Group=node_exporter\n
Type=simple\n
ExecStart=/usr/local/bin/node_exporter\n

[Install]\n
WantedBy=multi-user.target 
'''


def main():
    if get_exporter(url=exporter_url, file=exporter_file):
        if validate_sha(sha=exporter_sha, return_hash=get_checksum(exporter_file)):
            extract_file(file_name=exporter_file)
            move_files(wrk_dir=exporter_working_dir, bin_file=bin_file_name, final_bin_dir=bin_file_dest)
            create_new_user(new_user=username)
            usr_uid, grp_id = get_user_uid(u_name=username)
            file_set_owner(uid=usr_uid, grpid=grp_id, path='{}/{}'.format(bin_file_dest, bin_file_name))
            service_create(location=svc_location, srvice_name=svc_name, file_ext=svc_file_extention)
            service_start(svc=svc_name)
            service_status(svc=svc_name)
            service_enable(svc=svc_name)
            script_clean_up(tmp_dir=exporter_working_dir, tmp_gz=exporter_file)
        else:
            raise ValueError('The Hash no matchie')
    else:
        raise ValueError('Unable to get exporter')


def get_exporter(url=None, file=None):
    """Download the exporter"""
    try:
        if url and file:
            system('wget {}{}'.format(url, file))
            return True
    except OSError:
        print('Something went wrong with sending the command to the host')
        return False


def validate_sha(sha=None, return_hash=None):
    """Validate SHA256 hash from download"""
    if return_hash and sha and len(sha) == 64 and return_hash == sha:
        return True
    else:
        return False


def get_checksum(file_name=None):
    """Calculate sha256 checksum of file"""
    block_size = 65536
    sha256 = hashlib.sha256()
    try:
        with open(file_name, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
            return str(sha256.hexdigest())
    except IOError:
        print("Something went wrong with the file, don't think it's there")


def extract_file(file_name=None):
    """Extract file"""
    if file_name:
        try:
            with closing(tarfile.open(file_name)) as t:
                    t.extractall(path='./')
        except (tarfile.TarError, tarfile.ExtractError) as e:
            print(e)
    else:
        raise ValueError('File Name AND Path must be specified')


def move_files(wrk_dir=None, bin_file=None, final_bin_dir=None):
    """Move files to correct location"""
    from_path = '{}/{}'.format(wrk_dir, bin_file)
    to_path = '{}/{}'.format(final_bin_dir, bin_file)
    if os_path.isdir(wrk_dir) and os_path.isfile(from_path) and os_path.isdir(final_bin_dir):
        rename(from_path, to_path)
    else:
        raise ValueError('Something went wrong when I tried to move the files, check paths idiot.')


def _user_exists(new_user):
    """Validate user doesn't already exist"""
    try:
        pwd.getpwnam(new_user)
        return True
    except KeyError:
        return False


def get_user_uid(u_name):
    """Get linux user id for setting owner """
    uid = pwd.getpwnam(u_name).pw_uid
    grpid = grp.getgrnam(u_name).gr_gid
    return uid, grpid


def create_new_user(new_user):
    """Create Service User"""
    if _user_exists(new_user=username):
        print('user already exists')
    else:
        system('useradd --no-create-home --shell /bin/false {}'.format(new_user))


def file_set_owner(uid=None, grpid=None, path=None):
    """Set file owner
    chown node_exporter:node_exporter /usr/local/bin/node_exporter
    """
    chown(path, uid, grpid)


def service_create(location, srvice_name, file_ext):
    """Create service in /etc/systemd/system/node_exporter.service"""
    full_path = '{}{}{}'.format(location, srvice_name, file_ext)
    if os_path.isfile(full_path):
        print('service already exists')
    else:
        with open(full_path, 'w') as f:
            f.write(svc_definition)


def service_start(svc):
    """Reload daemon and start the service"""
    system('systemctl daemon-reload')
    system('systemctl start {}'.format(svc))


def service_status(svc):
    """Check status of service"""
    system('systemctl status {}'.format(svc))


def service_enable(svc):
    """Enable the service"""
    system('systemctl enable {}'.format(svc))


def script_clean_up(tmp_dir, tmp_gz):
    """Cleans up temp working directory and gz"""
    remove(tmp_gz)
    rmtree(tmp_dir)


if __name__ == '__main__':
    main()
