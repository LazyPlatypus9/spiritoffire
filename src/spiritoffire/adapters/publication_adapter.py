from typing import Generator, Optional

from spiritoffire.adapters import DatabaseAdapter
from spiritoffire.core.mongo_database import MongoDatabase
from spiritoffire.models.publication import Publication

class PublicationAdapter(DatabaseAdapter[Publication]):
    def __init__(self, mongo_database: MongoDatabase, app_name: str):
        self.collection = mongo_database.get_database(app_name)["publication"]

    def add(self, item: Publication) -> str:
        if not self.exists(item):
            result = self.collection.insert_one(item.model_dump(by_alias=True, exclude_none=True))
            return str(result.inserted_id)
        
        return item.id
    
    def get_all(self) -> Generator[Publication, None, None]:
        for document in self.collection.find({}):
            document['_id'] = str(document['_id'])
            yield Publication(**document)

    def exists(self, item: Publication) -> Optional[Publication]:
        document = self.collection.find_one({"callback_url": item.callback_url, "target": item.target})

        if document:
            return document
        return None