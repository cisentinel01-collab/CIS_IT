from models.base_model import BaseModel

class Settings(BaseModel):
    table_name = "settings"

    def get_settings(self):
        query = f"SELECT * FROM {self.table_name} LIMIT 1"
        results = self.db.execute_query(query)
        return results[0] if results else None

    def update_settings(self, data):
        settings = self.get_settings()
        if settings:
            self.update(settings['id'], data)
        else:
            self.create(data)
