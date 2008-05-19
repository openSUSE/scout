# import zypp

# class ZyppParser(object):
# 
#     rebuild_cache = False
# 
#     @classmethod
#     def list(cls):
#         z = zypp.ZYppFactory_instance().getZYpp()
#         repoManager = zypp.RepoManager()
#         repos = repoManager.knownRepositories()
# 
#         for repo in repos:
#             if not repo.enabled():
#                 continue
#             if cls.rebuild_cache and not repoManager.isCached(repo):
#                repoManager.buildCache(repo)
#             z.addResolvables(repoManager.createFromCache(repo).resolvables())
# 
#     print "Available items: %d" % ( z.pool().size() )
#     for item in z.pool():
#         print "* %s:%s-%s.%s\t(%s)" % ( item.resolvable().kind(),
#                                         item.resolvable().name(),
#                                         item.resolvable().edition(),
#                                         item.resolvable().arch(),
#                                         item.resolvable().repository().info().alias() )

class ScoutModule(object):

    name = "bin"
    desc = "Search for the binaries contained in the packages."

    @classmethod
    def main(cls, args):
        print "searching for term '%s'" % (args[1])
