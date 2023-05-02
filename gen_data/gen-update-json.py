import os
import json
import optparse
import utils
import arch

GIT_ROOT = utils.Popen( ["/usr/bin/git", "rev-parse", "--show-toplevel"] )
GIT_REMOTE_URL = utils.Popen( ["/usr/bin/git", "config", "--get", "remote.origin.url"] )
DIR = "."
VERBOSE = False
DISTRO_DATA_JSON = f"{GIT_ROOT}/distro-data.json"

def update_data_json(file_path: str) -> None:
    file_info = strip_info(file_path)
    json_data = json.load(open(f"{DISTRO_DATA_JSON}.json", 'r'))
    
    try:
        json_data[file_info[0]]
        json_data[file_info[0]][file_info[2]]
    except KeyError:
        json_data[file_info[0]] = { }
        json_data[file_info[0]][file_info[2]] = { }
    
    
    url = get_release_url(RELEASE_TAG, file_info[3])
    sha = utils.Popen( ["sha256sum", f"{file_path}"] ).split()[0]
    
    
    json_data[file_info[0]][file_info[2]][file_info[1]] = {
        "name": f"udroid-{file_info[0]}-{file_info[1]}",
        "friendlyName": f"{file_info[0]} {file_info[1]}",
        "url": url,
        "sha": sha
    }
    
    data_json = open(f"{DISTRO_DATA_JSON}.json", 'w')
    json.dump(json_data, data_json, indent=4)
    
def strip_info(file_path: str) -> list:
    basename = os.path.basename(file_path)
    name = os.path.splitext(basename)[0]
    name = os.path.splitext(name)[0]
    
    sp = name.split("-")
    StoPdict = arch.translated_arch()

    suite = sp[0]
    variant = sp[1]
    packageArchitecture = StoPdict[sp[2]]
    
    return [suite, variant, packageArchitecture, basename]

def get_release_url(release_tag: str, file_path: str) -> str:
    url = "{}/releases/download/{}/{}".format(GIT_REMOTE_URL, release_tag, file_path)
    
    return url
    
if __name__ == '__main__':
    # parse command line options
    parser = optparse.OptionParser()
    
    parser.add_option('-R', '--release-tag', dest='release_tag',
                          help='release tag', type=str)
    
    options, args = parser.parse_args()
    
    # get release tag
    RELEASE_TAG = options.release_tag
    for file_path in utils.getfilesR(DIR):
        if file_path.endswith(".tar.gz"):
            update_data_json1(file_path)
