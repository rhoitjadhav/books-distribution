from database import SessionLocal, Base


class RepositoryHelper:
    TABLE_MODEL_DICT = {
        mapper.class_.__tablename__: mapper.class_ for mapper in Base.registry.mappers
    }

    def create(self, table_name, values: dict):
        model = self.TABLE_MODEL_DICT.get(table_name)
        if not model:
            raise Exception(f"Model not found for table: {table_name}")

        with SessionLocal() as session:
            try:
                session.bulk_insert_mappings(model, values)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
