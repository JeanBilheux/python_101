import ipywidgets as ipyw
from IPython.display import display, HTML, clear_output
from _utils import js_alert


def wizard(config):
    WizardPanel(InstrumentPanel(config))
    return


class Config(object):
    ipts = None
    scan = None

class Panel:

    layout = ipyw.Layout(border="1px lightgray solid", margin='5px', padding='15px')
    button_layout = ipyw.Layout(margin='10px 5px 5px 5px')
    label_layout = ipyw.Layout(height='32px', padding='2px', width='300px')    
    
    def show(self):
        display(self.panel)
        
    def remove(self):
        for w in self.widgets:
            w.close()
        self.panel.close()
        
    def nextStep(self):
        raise NotImplementedError

class WizardPanel:
    
    label_layout = ipyw.Layout(height='35px', padding='8px', width='300px')
    
    def __init__(self, start_panel):
        display(ipyw.Label("Testing Panel Generator!", layout=self.label_layout))
        start_panel.show()
        return

class InstrumentPanel(Panel):

    instruments = dict(
        # vulcan = 'sns',
        snap = 'sns',
        cg1d = 'hfir',
        )
    
    def __init__(self, config):
        self.config = config
        explanation = ipyw.Label("Please chose the instrument", layout=self.label_layout)
        # self.text = ipyw.Text(value="CG1D", description="", placeholder="instrument name")
        self.text = ipyw.Select(value="CG1D", options=[i.upper() for i in self.instruments.keys()])
        self.ok = ipyw.Button(description='OK', layout=self.button_layout)
        self.widgets = [explanation, self.text, self.ok]
        self.ok.on_click(self.validate)
        self.panel = ipyw.VBox(children=self.widgets, layout=self.layout)
        
    def validate(self, s):
#        instrument = self.text.value.encode()
        instrument = self.text.value
        if instrument.lower() not in self.instruments.keys():
            s = "instrument %s not supported!" % instrument
#            print(s)
            js_alert(s)
        else:
            self.config.instrument = instrument.upper()
            self.config.facility = self.instruments[instrument.lower()].upper()
            self.remove()
            ipts_panel = IPTSpanel(self.config)
            ipts_panel.show()
        return

class IPTSpanel(Panel):
    
    def __init__(self, config):
        self.config = config
        explanation = ipyw.Label("Please input your experiment IPTS number", layout=self.label_layout)
        self.text = ipyw.Text(value="", description="IPTS-", placeholder="IPTS number")
        self.ok = ipyw.Button(description='OK', layout=self.button_layout)
        self.widgets = [explanation, self.text, self.ok]
        self.ok.on_click(self.validate_IPTS)
        self.panel = ipyw.VBox(children=self.widgets, layout=self.layout)
        
    def validate_IPTS(self, s):
        ipts1 = self.text.value.encode()
        facility = self.config.facility
        instrument = self.config.instrument
        path = os.path.abspath('/%s/%s/IPTS-%s' % (facility, instrument, ipts1))
        if not os.path.exists(path):
            s = "Cannot open directory %s ! Please check IPTS number" % path
            js_alert(s)
        else:
            self.config.ipts = ipts = ipts1
            # use your experiment IPTS number
            self.config.iptsdir = iptsdir = path
            # path to the directory with ct, ob, and df data files or subdirs
            datadir = self.config.datadir = os.path.join(iptsdir,"raw/")
            self.remove()
            # make sure there is ct scan directory
            self.config.ct_scan_root = ct_scan_root = os.path.join(datadir, 'ct_scans')
            ct_scan_subdirs = [d for d in os.listdir(ct_scan_root) if os.path.isdir(os.path.join(ct_scan_root, d))]
            self.config.ct_scan_subdirs = ct_scan_subdirs
#            scan_panel = ScanNamePanel(self.config)
#            scan_panel.show()
        return
