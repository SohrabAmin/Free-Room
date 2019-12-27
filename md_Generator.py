class Table:
    """
    A Markdown Table
    """
    def __init__(self):
        """
        Instantiate a Markdown Table
        """
        self.table = []


if __name__ == '__main__':
    file = open('Assets/markdown.md', 'r+')
    x = file.readlines()
    file.write('## Heading')
    print(x)