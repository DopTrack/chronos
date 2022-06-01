import os

# LOC_AUTOMATION = '/home/rvandenberg/DopTrack/GroundControl/Automation/'	# niet meer nodig, mag nu doptrack gebruiken
LOC_AUTOMATION = '/home/doptrack/DopTrack/GroundControl/Automation/'
LOC_PEN = LOC_AUTOMATION + 'REC_PENDING/'
LOC_ARM = LOC_AUTOMATION + 'REC_ARMED/'
LOC_REC = '/media/data/'

# LOC_ZIP = LOC_REC    # niet meer nodig ik kan nu in zip dir schrijven
LOC_ZIP = '/home/doptrack/www/Data_Download_Website/'

#LOC_IMAGE = '/var/www/archive_all'
LOC_IMAGE = '/home/doptrack/www/archive_all'
LOC_THUMB = '/home/doptrack/www/Data_Download_Website/thumb'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

