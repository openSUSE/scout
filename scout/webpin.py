# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout
import sys
import httplib
import urllib
from xml.dom import minidom

class ScoutModule(object):

    name = "webpin"
    desc = _("Search in packages using the webpin webservice.")
    distros = {
        'suse110' : 'openSUSE_110',
        'suse103' : 'openSUSE_103',
        'suse102' : 'openSUSE_102',
        'factory' : 'SUSE_Factory',
    }
    service_host = 'api.opensuse-community.org'
    service_baseurl = '/searchservice/Search/Simple/'


    @classmethod
    def query(cls, term, distro):
        try:
            url = cls.service_baseurl + cls.distros[distro] + '/' + urllib.quote(term)
            c = httplib.HTTPConnection(cls.service_host)
            c.connect()
            c.putrequest('GET', 'http://%s%s' % (cls.service_host, url))
            c.putheader('User-Agent', 'scout')
            c.putheader('Accept', 'text/xml')
            c.endheaders()
            r = c.getresponse()
            data = r.read()
            r.close()
            return minidom.parseString(data)
        except Exception, e:
            print _("Cannot retreive query results ... %s") % e
            return None

    @classmethod
    def fill_result(cls, root):
        scout.null_lang.install()
        result_list = [_("pkg"), _("ver"), _("arch"), _("repo"), _("files")]
        result_list2=[_("package"), _("version"), _("arch"), _("repository URL"), _("matched files")]
        scout.default_lang.install()
        result = scout.Result( result_list, result_list2 );

        for node in root.getElementsByTagName("package"):
            name = node.getElementsByTagName('name').item(0).childNodes.item(0).nodeValue
            version = node.getElementsByTagName('version').item(0).childNodes.item(0).nodeValue
            summary = node.getElementsByTagName('summary').item(0).childNodes.item(0).nodeValue
            repoURL = node.getElementsByTagName('repoURL').item(0).childNodes.item(0).nodeValue
            archs = []
            archsNode = node.getElementsByTagName('archs').item(0)
            if archsNode:
                for archNode in archsNode.getElementsByTagName('arch'):
                    archs.append(archNode.childNodes.item(0).nodeValue)
            archs = ' '.join(archs)
            fileMatches = []
            for matchedFileNameNode in node.getElementsByTagName('matchedFileName'):
                fileMatches.append(matchedFileNameNode.childNodes.item(0).nodeValue.strip())
            fileMatches = ' '.join(fileMatches)

            result.add_row([name, version, archs, repoURL, fileMatches]);

        return result

    @classmethod
    def main(cls, args=None):

        p = scout.Parser(cls.name)
        p.add_repos(['factory', 'suse110', 'suse103', 'suse102'])
        try:
            if not p.parse(args):
                return None
        except HelpOptionFound:
            p.print_help()
            sys.exit(1)

        term = p.args[0]

        repos = p.get_repos()
        if repos == None:
            return None
        for repo in repos:
            dom = cls.query(term, repo)
            root = dom.getElementsByTagNameNS('http://datastructures.pkgsearch.benjiweber.co.uk', 'packages').item(0)
            return cls.fill_result(root)

        return None
