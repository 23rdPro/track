import os


def get_text(field: str, aoc: str):
    qualifiers = ['beginner ', '', 'advanced ']
    text = field+' '+aoc
    for q in qualifiers:
        term = q+text
        article = term+' '+'~article'
        pdf = term+' '+'~pdf'
        klass = term+' '+'~class'
        video = term+' '+'~video'
        question = term+' '+'~question'
        yield [article, pdf, klass, video, question]


print(list(get_text('econometrics', 'monetary 1906'))[0])
print([text for text in get_text('econometrics', 'monetary 1906')])


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


def upload_to_path(instance, filename):
    return "pdfs/user_{0}/{1}".format(
        instance.author_id,
        filename,
    )


def run_check(result: list, link_set: dict):
    attributes = []
    for items in result:
        if items['link'] not in link_set:
            attributes.append((items['title'], items['link'], items['snippet']))
            link_set[items['link']] = items['link']
    return attributes
