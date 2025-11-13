# Example CRUD functions. Implement DB operations here.
# from sqlalchemy.orm import Session
# from . import models, schemas
#
# def get_example(db: Session, example_id: int):
#     return db.query(models.ExampleModel).filter(models.ExampleModel.id == example_id).first()
#
# def create_example(db: Session, obj_in: schemas.ExampleCreate):
#     db_obj = models.ExampleModel(**obj_in.dict())
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj

