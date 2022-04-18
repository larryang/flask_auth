""" test logging """
import os

def test_logfile_misc_debug():
    """ check if misc_debug.log exists """
    test_path = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(test_path, '../app/logs')
    filepath = os.path.join(log_dir, "misc_debug.log")
    assert os.path.isfile(filepath)
