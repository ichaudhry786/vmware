import os
import yaml
import logging

class Config:
  PSPHERE_CONFIG=None
  def __init__(self):
    logger = logging.getLogger(__name__)
    config_path = os.path.expanduser('config.yaml')
    try:
        config_file = open(config_path, "r")
        self.PSPHERE_CONFIG = yaml.load(config_file)
        config_file.close()
    except IOError:
        logger.warning("Configuration file %s could not be opened, perhaps you"
                   " haven't created one?" % config_path)
        PSPHERE_CONFIG = {"general": {}, "logging": {}}
        pass


  def _config_value(self,section, name, default=None):
    file_value = None
    if name in self.PSPHERE_CONFIG[section]:
        file_value = self.PSPHERE_CONFIG[section][name]

    if file_value:
        return file_value
    else:
        return default
