from google_cloud_api import GoogleSheetsAPI

class SelfCareSheet(object):
    def __init__(self, gs) -> None:
        self.gs: GoogleSheetsAPI = gs
        self.__scopes = self.gs.get_google_api_scopes

    @property
    def get_scopes(self):
        return self.__scopes


