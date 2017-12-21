from subprocess import call

modules = ['numpy', 'pandas', 'socket', 'numpy.random', 'random', 'watson_developer_cloud']

for module in modules:
    call('pip install ' + module)


