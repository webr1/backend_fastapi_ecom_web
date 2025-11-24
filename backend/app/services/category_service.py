from sqlalchemy.orm import Session
from typing import List
from ..schemas import CategoryResponse,CategoryCreate
from ..repositories.category_repository import CategoryRepository
from fastapi import HTTPException ,status




class CategoryServices:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)


    def get_all_category(self) -> List[CategoryResponse]:
        categories = self.repository.get_all()
        return [CategoryResponse.model_validate(cat) for cat in categories ]
    

    def get_category_by_id(self,category_id: int)-> CategoryResponse:
        category = self.repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not foud"
            )
        return CategoryResponse.model_validate(category)
    
    def create_category(self,category_data: CategoryCreate) -> CategoryResponse:
        category = self.repository.careate(category_data)
        return CategoryResponse.model_validate(category)

    

