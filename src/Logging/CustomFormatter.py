from colorlog import ColoredFormatter

class CustomFormatter(ColoredFormatter):
    COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'white',
        'SUCCESS': 'green',
        'STATUS': 'yellow',
        'WARNING': 'yellow',
        'ERROR': 'bold_red',
        'CRITICAL': 'red',
    }

    def __init__(self, *args, **kwargs):
        if 'log_colors' not in kwargs:
            kwargs['log_colors'] = self.COLORS

        super(CustomFormatter, self).__init__(*args, **kwargs)