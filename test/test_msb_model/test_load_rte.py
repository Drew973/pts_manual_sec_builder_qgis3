if __name__=='__console__':
        
    from manual_sec_builder.msb_model import msb_model
    
    m = msb_model.msbModel()
    p = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\Run005.rte'
    with open(p,'r') as f:
        m.loadRte(f)