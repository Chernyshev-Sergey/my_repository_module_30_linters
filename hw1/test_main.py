from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [
        {
            "id": 3,
            "name_of_the_dish": "каша рисовая",
            "cooking_time_in_minutes": "61",
            "number_of_views": response.json()[0]['number_of_views'],
        },
        {
            "id": 1,
            "name_of_the_dish": "Борщ",
            "cooking_time_in_minutes": "60",
            "number_of_views": 2,
        },
        {
            "id": 2,
            "name_of_the_dish": "Рассольник",
            "cooking_time_in_minutes": "50",
            "number_of_views": 2,
        },
        {'cooking_time_in_minutes': '15',
         'id': 4,
         'name_of_the_dish': 'каша гречневая',
         'number_of_views': 0}
    ]


def test_read_main_recipes_id():
    response = client.get("/recipes/3")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "name_of_the_dish": "каша рисовая",
        "cooking_time_in_minutes": "61",
        "list_of_ingredients": "рис",
        "description": "нет описания",
    }


if __name__ == "__main__":
    test_read_main_recipes()
    test_read_main_recipes_id()
