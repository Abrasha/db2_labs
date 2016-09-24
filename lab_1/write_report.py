from bs4 import BeautifulSoup


def write_report(data):
    """
    :param data: map of: url => (text_tags[], img_tags[])
    :return: BeautifulSoup formatted report
    """
    report = BeautifulSoup(features='xml')
    root_tag = report.new_tag('data')

    for url in data:
        text_tags, img_tags = data[url]

        page_tag = report.new_tag('page', url=url)
        root_tag.append(page_tag)

        for text in text_tags:
            tag = report.new_tag('fragment', type='text')
            tag.string = text.string
            page_tag.append(tag)

        for img in img_tags:
            tag = report.new_tag('fragment', type='image')
            tag.string = img.get('src')
            page_tag.append(tag)

    report.append(root_tag)

    return report
