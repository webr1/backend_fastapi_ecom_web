from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import (
    ProductResponse,
    ProductListResponse,
    ProductCreate,
)


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(self) -> ProductListResponse:
        products = self.product_repository.get_all()
        products_response = [
            ProductResponse.model_validate(prod) for prod in products
        ]
        return ProductListResponse(
            products=products_response,
            total=len(products)
        )

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        # check category exists
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {product_data.category_id} does not exist."
            )

        product = self.product_repository.create(product_data)
        return ProductResponse.model_validate(product)

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found."
            )
        return ProductResponse.model_validate(product)

    # def get_products_by_category(self, category_id: int) -> ProductListResponse:
    #     # проверяем что категория существует
    #     category = self.category_repository.get_by_id(category_id)
    #     if not category:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Category with id {category_id} not found."
    #         )

    #     # предполагается, что category_repository.get_by_category возвращает список продуктов
    #     products = self.category_repository.get_by_id(category_id)

    #     # преобразуем каждый продукт в ProductResponse
    #     products_response = [
    #         ProductResponse.model_validate(prod) for prod in products
    #     ]

    #     return ProductListResponse(products=products_response, total=len(products_response))

    def get_products_by_category(self, category_id: int) -> ProductListResponse:
        # проверяем, что категория существует
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found."
            )

        # получаем продукты по категории ИЗ ProductRepository
        products = self.product_repository.get_by_category(category_id)

        products_response = [
            ProductResponse.model_validate(prod) for prod in products
        ]

        return ProductListResponse(
            products=products_response,
            total=len(products_response)
        )
