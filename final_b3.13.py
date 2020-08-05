class Tag:
    def __init__(self, tag, is_single=False, toplevel=False, klass=None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.toplevel = toplevel
        self.attributs = {}
        self.text = ""
        self.childrens = []
        if klass is not None:
            self.attributs["class"] = " ".join(klass)
        for attr, val in kwargs.items():
            self.attributs[attr] = val

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.toplevel:
            res_str = ("<{tag}>".format(tag=self.tag))
            for child in self.childrens:
                res_str += str(child)
            res_str += ("</{tag}>".format(tag=self.tag))
            return res_str

    def __add__(self, other):
        self.childrens.append(other)
        return self

    def __str__(self):
        attrs = []
        for attr, val in self.attributs.items():
            attrs.append("%s='%s'" % (attr, val))
        attrs = " ".join(attrs)
        if self.childrens:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "{text}".format(text=self.text) + '\n'
            for child in self.childrens:
                internal += str(child)
            ending = "</{tag}>".format(tag=self.tag)
            result_str = opening + internal + ending
        else:
            if self.is_single:
                result_str = "\t" + "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            else:
                result_str = "\t" + "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)
        return result_str + '\n'


class HTML(Tag):

    def __init__(self, output=None):
        self.tag = "html"
        self.is_single = False
        self.toplevel = True
        self.output = output
        self.childrens = []
        self.attributs = {}
        self.text = ""


class TopLevelTag(Tag):
    def __init__(self, tag):
        self.is_single = False
        self.toplevel = False
        self.tag = tag
        self.childrens = []
        self.attributs = {}
        self.text = ""


if __name__ == "__main__":
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "Hello"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "Another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img
                body += div
            doc += body

    if doc.output is not None:
        with open(doc.output, 'w') as file:
            file.write(str(doc))
        print('Printout saved to file:', doc.output)
    else:
        print(doc)