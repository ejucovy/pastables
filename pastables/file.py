from paste.fileapp import FileApp
def app_factory(global_conf, **local_conf):
    return FileApp(local_conf['document'])
