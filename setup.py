#import subprocess


def greece_rte_ok() -> bool:
    try:
        import greece_rte
        return True
    except ImportError:
        return False
    

#(re) install greece_rte with pip from .whl
def install_greece_rte():
    setup_file = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\setup.bat'
    os.system(setup_file)





import os
setup_file = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\setup.bat'
#subprocess.run(setup_file , capture_output=True)
os.system(setup_file)
print('ok')