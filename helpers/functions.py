import hashlib
import os

from django.core.exceptions import ValidationError


def validate_file_handler(file):
    extn = os.path.splitext(file.name)[1]
    valid_extns = ['.pdf', ]
    if not extn.lower() in valid_extns:
        raise ValidationError('Unsupported File Extension.')


def make_key(key: str, key_prefix: str, version: int):
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
    return "pdfs/user_{0}/{1}".format(instance.author_id, filename)
