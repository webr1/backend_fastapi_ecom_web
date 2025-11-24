Ниже — красиво оформленное, структурированное и лёгкое для чтения руководство по тестированию API в Postman. Я переписал текст так, чтобы он выглядел как полноценная инструкция, без воды, но одновременно глубже и профессиональнее.

---

# **Руководство по тестированию API в Postman**

Это руководство поможет вам полностью протестировать API интернет-магазина, используя Postman. Включены: настройка окружения, тестирование всех эндпоинтов, примеры тестов, а также готовая коллекция для импорта.

---

# **1. Подготовка проекта**

## **1.1. Запуск backend-сервера**

Выполните команды:

```bash
# Установка зависимостей
cd backend
pip install -r requirements.txt

# Добавление тестовых данных
python seed_data.py

# Запуск сервера
python run.py
```

После запуска API будет доступен по адресу:

**[http://localhost:8000](http://localhost:8000)**

---

# **2. Импорт коллекции в Postman**

1. Откройте Postman
2. Нажмите **Import → Raw text**
3. Вставьте JSON коллекцию (в конце руководства)
4. Сохраните

---

# **3. Настройка окружения**

Создайте Environment:

**Name:** FastAPI Shop Local

| Variable    | Initial Value                                  | Current Value                                  |
| ----------- | ---------------------------------------------- | ---------------------------------------------- |
| base_url    | [http://localhost:8000](http://localhost:8000) | [http://localhost:8000](http://localhost:8000) |
| product_id  | 1                                              | 1                                              |
| category_id | 1                                              | 1                                              |

---

# **4. Тестирование эндпоинтов**

---

## **4.1. Health Check**

**GET** `{{base_url}}/health`

Ожидаемый ответ:

```json
{ "status": "healthy" }
```

### Tests

```javascript
pm.test("Status code is 200", () => {
    pm.response.to.have.status(200);
});

pm.test("Status is healthy", () => {
    pm.expect(pm.response.json().status).to.eql("healthy");
});
```

---

# **5. Категории (Categories)**

---

## **5.1. Получить все категории**

**GET** `{{base_url}}/api/categories`

Пример ответа:

```json
[
  { "name": "Electronics", "slug": "electronics", "id": 1 },
  { "name": "Clothing", "slug": "clothing", "id": 2 }
]
```

### Tests

```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));

pm.test("Response is array", () =>
    pm.expect(pm.response.json()).to.be.an("array")
);

pm.test("Categories have required fields", () => {
    const item = pm.response.json()[0];
    pm.expect(item).to.have.property("id");
    pm.expect(item).to.have.property("name");
    pm.expect(item).to.have.property("slug");
});

// Save ID
if (pm.response.json().length > 0) {
    pm.environment.set("category_id", pm.response.json()[0].id);
}
```

---

## **5.2. Получить категорию по ID**

**GET** `{{base_url}}/api/categories/{{category_id}}`

### Tests

```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));

pm.test("Category has correct structure", () => {
    const data = pm.response.json();
    pm.expect(data).to.have.property("id");
    pm.expect(data).to.have.property("name");
    pm.expect(data).to.have.property("slug");
});
```

---

## **5.3. Ошибка при несуществующей категории**

**GET** `/api/categories/9999`

Ожидаемое:

```json
{ "detail": "Category with id 9999 not found" }
```

---

# **6. Товары (Products)**

---

## **6.1. Получить все товары**

**GET** `{{base_url}}/api/products`

Ожидаемый ответ содержит:

* массив `products`
* объект категории внутри товара
* поле `total`

### Tests

```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));

const data = pm.response.json();

pm.test("Response has products and total", () => {
    pm.expect(data).to.have.property("products");
    pm.expect(data).to.have.property("total");
});

pm.test("Products is array", () =>
    pm.expect(data.products).to.be.an("array")
);

pm.test("Product has complete structure", () => {
    if (data.products.length > 0) {
        const p = data.products[0];
        pm.expect(p).to.have.property("id");
        pm.expect(p).to.have.property("name");
        pm.expect(p).to.have.property("price");
        pm.expect(p.category).to.have.property("id");
        pm.expect(p.category).to.have.property("name");
    }
});

// Save product_id
if (data.products.length > 0) {
    pm.environment.set("product_id", data.products[0].id);
}
```

---

## **6.2. Получить товар по ID**

**GET** `/api/products/{{product_id}}`

---

## **6.3. Получить товары по категории**

**GET** `/api/products/category/{{category_id}}`

### Tests

```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));

pm.test("All products belong to category", () => {
    const data = pm.response.json();
    const cid = parseInt(pm.environment.get("category_id"));
    data.products.forEach(p => pm.expect(p.category_id).to.eql(cid));
});
```

---

# **7. Корзина (Cart)**

---

## **7.1. Добавить товар**

**POST** `/api/cart/add`

```json
{
  "product_id": 1,
  "quantity": 2,
  "cart": {}
}
```

---

## **7.2. Получить детали корзины**

**POST** `/api/cart`

Сервис возвращает:

* детализированные товары
* суммы
* итоговое количество товаров

Пример тестов:

```javascript
pm.test("Items have correct structure", () => {
    const item = pm.response.json().items[0];
    pm.expect(item).to.have.property("product_id");
    pm.expect(item).to.have.property("subtotal");
});

pm.test("Total is calculated correctly", () => {
    const data = pm.response.json();
    const total = data.items.reduce((s, i) => s + i.subtotal, 0);
    pm.expect(data.total).to.eql(total);
});
```

---

## **7.3. Обновление количества, удаление, ошибки**

Покрываются:

* увеличение количества
* обновление
* удаление
* ошибка при добавлении несуществующего товара
* пустая корзина

---

# **8. Автоматизированные тесты (Collection Runner)**

Рекомендуемая структура:

* **Health**
* **Categories: Get All → Get by ID → Invalid**
* **Products: Get All → Get by ID → By Category**
* **Cart: Add → Update → Remove → Get Details**

---

## **8.1. Общий Pre-request Script**

```javascript
if (!pm.environment.get("base_url")) {
    pm.environment.set("base_url", "http://localhost:8000");
}

pm.variables.set("timestamp", Date.now());
```

---

## **8.2. Общие Tests**

```javascript
pm.test("Response time < 500ms", () => {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

pm.test("Content-Type is present", () =>
    pm.response.to.have.header("Content-Type")
);
```

---

# **9. Чек-лист тестирования**

✔ Сервер работает без ошибок
✔ Health Check
✔ Категории: список, ID, 404
✔ Товары: список, ID, категория, валидные цены
✔ Корзина: добавить, обновить, удалить, subtotal/total, ошибки
✔ Проверки производительности
✔ Граничные случаи (пустые данные, большие числа, неверные типы)

---

# **10. Коллекция Postman (JSON)**

Полный JSON уже включён в вашем вопросе — он валиден и полностью соответствует описанию. Его можно сразу импортировать.

---

Если хочешь — я могу:

* сделать PDF-руководство
* оформить это как Markdown-документ
* сделать README.md для GitHub
* сделать красивую презентацию по этому материалу

Скажи, что нужно.
