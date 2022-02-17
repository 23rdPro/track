import hashlib
import os
import random
import string


def _hash(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def new_key():
    return 'track.key' + _hash()


def make_key(key, key_prefix, version):
    joint = ':'.join([key_prefix, '%s' % version, key])
    work = hashlib.blake2b(digest_size=20)
    work.update(joint.encode())
    return work.hexdigest()


def get_text(field: str, aoc: str):
    qualifiers = ['', 'advanced ']
    text = field+' '+aoc
    for q in qualifiers:
        term = q+text
        article = term+' '+'~article'
        pdf = term+' '+'~pdf'
        klass = term+' '+'~class'
        video = term+' '+'~video'
        question = term+' '+'~question'
        yield [article, pdf, klass, video, question]


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


def upload_to_path(instance, filename):
    return "pdfs/user_{0}/{1}".format(
        instance.author_id,
        filename,
    )
