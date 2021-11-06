import os


def get_text(field: str, aoc: str):
    qualifiers = ['beginner ', '', 'advanced ']  # todo, more qualifiers
    text = field+' '+aoc
    for q in qualifiers:
        term = q+text
        pdf = term+' '+'~pdf'
        klass = term+' '+'~class'
        video = term+' '+'~video'
        yield [term, pdf, klass, video]


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


def upload_to_path(instance, filename):
    return "pdfs/user_{0}/{1}".format(
        instance.author_id,
        filename,
    )