from typing import Union, Annotated

from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/products/{id}")
def detail_view(id: int) -> dict:
    return {"product": f'Stock number {id}'}

@app.get("/users/{name}")
def users(name: str, age: int) -> dict:
    return {
        "user_name": name,
        "user_age": age
    }

# Напишите код приложения на FastAPI, в котором асинхронная функция list_cities()
# будет принимать GET запрос по маршруту /country/<country>,
# получая строковой параметр country из параметра пути, а числовой параметр limit из параметра запроса.
# Конечная точка должна возвращать словарь с ключом country и значением параметра country,
# и с ключом cities и значением в виде списка городов, полученных из словаря country_dict для данной страны.
# Количество городов в списке ответа должно быть ограничено параметром limit.
# P.S. На экран ничего не нужно выводить, пример запроса:
# GET /country/Russia?limit=3
# ответ для него:
# {'country': Russia', 'cities': ['Moscow', 'St. Petersburg', 'Novosibirsk']}
# Пример словаря country_dict.
# country_dict = {
#     'Russia': ['Moscow', 'St. Petersburg', 'Novosibirsk', 'Ekaterinburg', 'Kazan'],
#     'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia'],
# }
@app.get("/country/{country}")
async def list_cities(country: str, limit: int) -> dict:
    country_dict = {
        'Russia': ['Moscow', 'St. Petersburg', 'Novosibirsk', 'Ekaterinburg', 'Kazan'],
        'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia'],
    }

    return {
        "country": country,
        "cities": [] if country not in country_dict.keys() else country_dict[country][:limit]
    }



# Напишите код приложения на FastAPI, в котором асинхронная функция user()
# будет принимать GET-запрос по маршруту /user/<name>, получая строковой параметр пути name и
# использует валидатор Path со следующими параметрами:
# Минимальная длина строки 4 символа
# Максимальная длина строки 20 символов
# Описание поля Enter your name
# Конечная точка должна возвращать словарь с ключом user_name и значением параметра name.
#
# Пример запроса:
# /user/Alex
# ответ для него:
# {'user_name': 'Alex'}
@app.get("/user/{name}")
async def user(
    name: Annotated[str, Path(min_length=4, max_length=20, description="Enter your name", pattern=r"^[A-ZА-ЯЁ][a-zа-яё]*$")]
) -> dict:
    return {"user_name": name}

# Напишите код приложения на FastAPI, в котором асинхронная функция category()
# будет принимать GET-запрос по маршруту /category/<category_id>/products,
# получая числовой параметр пути category_id и числовой параметр запроса page.
# Для параметра category_id используется валидатор Path со следующими параметрами:
# Значение должно быть больше 0
# Описание поля: "Category ID"
# Для параметра page валидатор не нужен.
# Конечная точка должна возвращать словарь с ключом 'category_id' и значением параметра category_id,
# и ключом 'page' и значением параметра page.
# Пример запроса:
# /category/3/products?page=7
# ответ для него:
# {'category_id': 3, 'page': 7}
@app.get("/category/{category_id}/products")
async def category(page: int, category_id: Annotated[int, Path(gt=0, description="Category ID")]) -> dict:
    return {"category_id": category_id, "page": page}




