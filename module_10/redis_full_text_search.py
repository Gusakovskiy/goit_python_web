from dataclasses import dataclass
from string import punctuation
from typing import List

from faker import Faker

from module_10.redis_client import client

fake = Faker()


_DOC_TEMPLATE = 'doc_{}'


def _get_tokens(value: str) -> List[str]:
    result = []
    for ch in punctuation:
        value = value.replace(ch, '')
    value = value.strip()
    for word in value.split(' '):
        result.append(word.lower())
    return result


def _convert_from_redis(redis_values):
    # redis client return everything as bytes
    return {
        el.decode('utf-8')
        for el in redis_values
    }


def _search_in_index(query):
    tokens = _get_tokens(query)
    return _convert_from_redis(client.sinter(*tokens))


@dataclass(frozen=True)
class Document:
    id: int
    first_name: str
    last_name: str
    job_title: str

    @property
    def search_fields(self):
        return (
            self.first_name,
            self.last_name,
            self.job_title,
        )

    @property
    def tokens(self):
        all_tokens = []
        for field in self.search_fields:
            all_tokens.extend(_get_tokens(field))
        return all_tokens

    @property
    def search_field(self):
        return ' '.join(self.tokens)

    @property
    def key(self) -> str:
        return _DOC_TEMPLATE.format(self.id)


def _get_documents():
    num_noise_docs = 10
    documents = [
        Document(
            id=1,
            first_name='Liza',
            last_name='Clonie',
            job_title='Actress',
        ),
        Document(
            id=2,
            first_name='Brad',
            last_name='Fox',
            job_title='Cascader',
        ),
        Document(
            id=3,
            first_name='Michelle',
            last_name='Musk',
            job_title='Red Fox',
        ),
    ]
    number_existing_docs = len(documents)
    documents = documents + [
        Document(
            id=_id,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            job_title=fake.job(),
        )
        for _id in range(number_existing_docs + 1, number_existing_docs + num_noise_docs)
    ]
    return documents


def push_data():
    print('Start add data')
    for doc in _get_documents():
        pipeline = client.pipeline()  # redis transaction
        pipeline.multi()
        for token in doc.tokens:
            client.sadd(doc.key, token)  # To be able to update docs
            # build inverted index
            client.sadd(token, doc.key)
            # for more advance text search use ZADD
        pipeline.execute(raise_on_error=True)
        print('Added ', doc.tokens)
    print('Finish adding data')
    print(' ')


def update_doc(doc):
    new_tokens = set(doc.tokens)
    old_tokens = _convert_from_redis(client.smembers(doc.key))
    to_delete = old_tokens.difference(new_tokens)
    pipeline = client.pipeline()  # redis transaction
    pipeline.multi()
    for token in to_delete:
        client.srem(doc.key, token)
        client.srem(token, doc.key)
    to_add = new_tokens.difference(old_tokens)
    for token in to_add:
        client.sadd(doc.key, token)
        client.sadd(token, doc.key)
    pipeline.execute(raise_on_error=True)


def search_queries(queries):
    print(' ')
    print('*' * 42)

    for query in queries:
        result = _search_in_index(query)
        # for union use client.sunion(_get_tokens(query))
        print(f'Search query: {query}, {result}')
    print('*' * 42)


if __name__ == '__main__':
    # before start remove everything from  db
    client.flushdb()
    # https://redis.com/redis-best-practices/indexing-patterns/full-text-search/
    push_data()
    queries = (
        'Liza',
        'Brad Fox',
        'Fox',
        'Foxes',
        'Layer',  # maybe from random data
        'Nurse',  # maybe from random data
        'Wick',  # Doesn't exists
        'Liza Cascader',  # from different documents
        'Clonie Musk',  # from different documents
    )
    search_queries(queries)
    doc = Document(
        id=1,
        first_name='Liza',
        last_name='Bunny',
        job_title='Scientist',
    )
    update_doc(doc)
    queries = (
        'Bunny',
        'Scientist'
    )
    search_queries(queries)
