import pytest

from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(client):
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def more_news(client):
    today = datetime.today()
    news_list = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_list.append(News.objects.create(
            title=f'Новость {index}',
            text='Текст',
            date=today - timedelta(days=index))
        )
    return news_list


@pytest.fixture
def comment(author, news):
    # news = News.objects.create(title='Заголовок', text='Текст')
    comment = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария'
        )
    return comment


@pytest.fixture
def more_comment(author, news):
    now = timezone.now()
    comment_list = []
    for index in range(2):
        comment = Comment.objects.create(
                news=news,
                author=author,
                text=f'Tекст {index}',
            )
        comment.created = now + timedelta(days=index)
        comment.save()
        comment_list.append(comment)
    return comment_list


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст комментария',
    }
