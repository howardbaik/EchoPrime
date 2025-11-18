# Suppress multiprocessing resource tracker warnings early (common with scikit-learn/joblib)
import warnings
import sys

# Suppress all UserWarnings from multiprocessing.resource_tracker module
warnings.filterwarnings('ignore', category=UserWarning, module='multiprocessing.resource_tracker')
# Also suppress by message pattern (more reliable)
warnings.filterwarnings('ignore', message='.*resource_tracker.*')
warnings.filterwarnings('ignore', message='.*leaked semaphore.*')
warnings.filterwarnings('ignore', message='.*leaked.*objects to clean up.*')

# Use a custom warning handler to catch shutdown warnings that bypass filters
_original_showwarning = warnings.showwarning
def _filter_resource_tracker_warnings(message, category, filename, lineno, file=None, line=None):
    """Filter out resource tracker warnings"""
    msg_str = str(message) if message else ''
    # Handle filename as string, Path object, or None
    if filename:
        try:
            filename_str = str(filename)
        except:
            filename_str = repr(filename)
    else:
        filename_str = ''
    
    # Check if this is a resource tracker warning by message content or filename
    is_resource_tracker_warning = (
        category == UserWarning and (
            'resource_tracker' in msg_str.lower() or 
            'resource_tracker' in filename_str.lower() or
            'leaked semaphore' in msg_str.lower() or
            ('leaked' in msg_str.lower() and 'clean up' in msg_str.lower())
        )
    )
    
    if is_resource_tracker_warning:
        return  # Suppress the warning
    
    _original_showwarning(message, category, filename, lineno, file, line)

warnings.showwarning = _filter_resource_tracker_warnings

from .model import EchoPrime
from .model import EchoPrimeTextEncoder