""" test logging """
import os


def test_logfile_exists():
    """ test if logfile and directory exists """
    test_path = os.path.dirname(os.path.abspath(__file__))

    # check directory
    log_dir = os.path.join(test_path, '../app/logs')
    assert os.path.exists(log_dir)

    # check log file
    filepath = os.path.join(log_dir, "info.log")
    assert os.path.isfile(filepath)
