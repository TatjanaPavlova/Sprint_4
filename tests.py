import pytest
from main import BooksCollector

class TestBooksCollector:

    def test_add_new_book_add_duplicate_book_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Вино из одуванчиков')
        collector.add_new_book('Вино из одуванчиков')
        
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize(
            'name,genre', 
            [
                ('Убийство в Восточном экспрессе', 'Детективы'), 
                ('Солярис', 'Фантастика'), 
                ('Дракула', 'Ужасы')
            ]
        )
    def test_set_book_genre_three_books_with_existed_genres_added(self, name, genre):
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        
        assert collector.get_book_genre(name) == genre

    def test_set_book_genre_book_with_non_existed_genre_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Праздник, который всегда с тобой')
        collector.set_book_genre('Праздник, который всегда с тобой', 'Автобиография')
        
        assert collector.get_book_genre('Праздник, который всегда с тобой') == ''

    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Двенадцать стульев')
        collector.books_genre['Двенадцать стульев'] = 'Комедии'
        
        assert collector.get_book_genre('Двенадцать стульев') == 'Комедии'

    def test_get_books_with_specific_genre_no_books_with_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер и методы рационального мышления')
        collector.add_new_book('Трое из Простоквашино')
        collector.set_book_genre('Гарри Поттер и методы рационального мышления', 'Фантастика')
        collector.set_book_genre('Трое из Простоквашино', 'Мультфильмы')

        result = collector.get_books_with_specific_genre('Детективы')
        assert result == []

    @pytest.mark.parametrize(
        'books_and_genres', 
        [
            [('Смерть на Ниле', 'Детективы'), ('Тайна третьей планеты', 'Фантастика')],
            [('Бесприданница', ''), ('Оно', 'Ужасы'), ('Сияние', 'Ужасы')]
        ]
    )
    def test_get_books_genre_returns_correct_books_and_genres(self, books_and_genres):
        collector = BooksCollector()
        
        for name, genre in books_and_genres:
            collector.add_new_book(name)
            if genre:
                collector.set_book_genre(name, genre)
        
        expected = {name: genre for name, genre in books_and_genres}
        assert collector.get_books_genre() == expected

    def test_get_books_for_children_if_in_age_rating_then_not_shown(self):
        collector = BooksCollector()
        collector.add_new_book('Алиса в Зазеркалье')
        collector.add_new_book('Кошмар на улице Вязов')
        collector.set_book_genre('Алиса в Зазеркалье', 'Мультфильмы')
        collector.set_book_genre('Кошмар на улице Вязов', 'Ужасы')

        assert collector.get_books_for_children() == ['Алиса в Зазеркалье']
    
    @pytest.mark.parametrize(
        'name', 
        [
            ('Москва — Петушки',), 
            ('Мечтают ли андроиды об электроовцах?',), 
            ('Пятьдесят оттенков серого',)
        ]
    )
    def test_add_book_in_favorites_one_book_added(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)

        assert collector.get_list_of_favorites_books() == [name]

    def test_delete_book_from_favorites_book_removed(self):
        collector = BooksCollector()
        collector.add_new_book('Человек, который принял жену за шляпу')
        collector.add_new_book('Аристотель и муравьед едут в Вашингтон')
        collector.add_book_in_favorites('Человек, который принял жену за шляпу')
        collector.add_book_in_favorites('Аристотель и муравьед едут в Вашингтон')
        collector.delete_book_from_favorites('Аристотель и муравьед едут в Вашингтон')

        assert collector.get_list_of_favorites_books() == ['Человек, который принял жену за шляпу']

    def test_get_list_of_favorites_books_returns_correct_list(self):
        collector = BooksCollector()

        books = [
            'Мой дедушка был вишней',
            'Пеппи Длинныйчулок',
            'Путешествие к центру Земли',
            'Фантастические твари и где они обитают',
            'Пикник на обочине'
        ]
        for book in books:
            collector.add_new_book(book)

        collector.add_book_in_favorites('Пикник на обочине')
        collector.add_book_in_favorites('Фантастические твари и где они обитают')

        assert collector.get_list_of_favorites_books() == [
            'Пикник на обочине',
            'Фантастические твари и где они обитают'
        ]