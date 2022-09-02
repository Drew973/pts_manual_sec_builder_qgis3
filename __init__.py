#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# For relative imports to work in Python 3.6

#changing sys.path can affect other plugins and manager!

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load manual_sec_builder class from file manual_sec_builder.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .manual_sec_builder import manual_sec_builder#class
    return manual_sec_builder(iface)
