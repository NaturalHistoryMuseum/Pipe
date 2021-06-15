from ._base import BaseAttributeCluster


class AuthorAttributeCluster(BaseAttributeCluster):
    attribute_name = 'author'

    @staticmethod
    def tokenise(input_string):
        if input_string == '' or input_string is None:
            return []
        split_authors = []
        for a in input_string.split(';'):
            family_name, given_names = a.strip().split(',', 1)
            given_names = ' '.join([n[0] for n in given_names.split(' ') if len(n) > 0])
            rearranged = ' '.join([given_names.strip(), family_name.strip()]).strip()
            if rearranged != '':
                split_authors.append(rearranged)
        return split_authors
