from urllib.request import urlopen
from json import loads
from re import split


def resolve_version(package_name):
    max_major = 0
    max_version = tuple()
    url_address = "https://api.nuget.org/v3-flatcontainer/{}/index.json".format(package_name)
    try:
        with urlopen(url_address) as web_content:
            data = web_content.read()
            encoding = web_content.info().get_content_charset('utf-8')
            version_list = loads(data.decode(encoding))['versions']
            for version in version_list:
                (major, minor, *patch_prefix, patch) = split("\.", version)
                if int(major) >= int(max_major):
                    max_major = major
                    p_prefix = ''
                    if len(patch_prefix) != 0:
                        for p in patch_prefix:
                            p_prefix += str(p)

                    max_version = (major, minor, p_prefix, patch)

    except:
        return -2, -2, '', -2

    return max_version
