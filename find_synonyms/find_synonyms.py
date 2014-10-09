#!/usr/bin/python
"""
Let's find synonyms in address field :)
"""
from sklearn import tree

FIND_SYNONYMS_DIR = "./"
DUPLICATE_ADDRESS_FILE = FIND_SYNONYMS_DIR + "duplicate_addresses.txt"


def find_synonyms_in_address():
    # from_dup_addr_to_train_set()
    train_file = FIND_SYNONYMS_DIR + 'train.txt'
    clf = train_synonym_classifier(train_file, 0, 180)
    with open(FIND_SYNONYMS_DIR + "iris.dot", 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)
    evaluate(clf, train_file, 180, 200)
    from_dup_addr_to_synonyms

def from_dup_addr_to_train_set():
    with open(DUPLICATE_ADDRESS_FILE, 'r') as f:
        for line in f:
            addr1_tokens, addr2_tokens = map(
                lambda s:s.strip().lower().split(' '),
                line.split('\t')
            )
            if len(addr1_tokens) != len(addr2_tokens):
                continue
            token_pairs = zip(addr1_tokens, addr2_tokens)
            for i in range(len(token_pairs)):
                token1, token2 = token_pairs[i]
                token1, token2 = token1.strip('.,'), token2.strip('.,')
                if is_synonyms_in_address(token1, token2):
                    print token1, token2
                    # print addr1_tokens, addr2_tokens


def from_dup_addr_to_synonyms(clf):
    with open(DUPLICATE_ADDRESS_FILE, 'r') as f:
        for line in f:
            addr1_tokens, addr2_tokens = map(
                lambda s:s.strip().lower().split(' '),
                line.split('\t')
            )
            if len(addr1_tokens) != len(addr2_tokens):
                continue
            token_pairs = zip(addr1_tokens, addr2_tokens)
            for i in range(len(token_pairs)):
                token1, token2 = token_pairs[i]
                token1, token2 = token1.strip('.,'), token2.strip('.,')
                if is_synonyms_in_address(token1, token2):
                    print token1, token2, i, len(token_pairs)-i-1
                    # print addr1_tokens, addr2_tokens

def is_synonyms_in_address(token1, token2):
    if token1 == token2:
        return False
    if is_integer(token1) and is_integer(token2):
        return False
    
    return True


def evaluate(clf, test_set, begin, end):
    features, labels, originals = file_to_feature_and_label(test_set, begin, end)
    count_correct = 0
    for feature_set, original, label in zip(features, originals, labels):
        predicted_label,  = clf.predict(feature_set)[0]
        print predicted_label, label, original
        if predicted_label == label:
            count_correct += 1
    print str(count_correct) + '/' + str(end - begin) + ' corrects'

def train_synonym_classifier(train_data_file, begin, end):
    features, labels, originals = file_to_feature_and_label(train_data_file, begin, end)
    clf = tree.DecisionTreeClassifier()
    return clf.fit(features, labels)


def file_to_feature_and_label(train_data_file, begin, end):
    originals = []
    features = []
    labels = []
    count = 0
    with open(train_data_file, 'r') as f:
        for line in f:
            count += 1
            if begin <= count and count < end:
                label, token1, token2, pos_l, pos_r = line.strip().split(' ')
                originals.append([label, token1, token2, pos_l, pos_r])
                features.append(generate_feature_vector(token1, token2, pos_l, pos_r))
                labels.append(label)         
    return features, labels, originals


def generate_feature_vector(token1, token2, pos_l, pos_r):
    features = []
    features.append(len(token1))
    features.append(len(token2))
    features.append(pos_l)
    features.append(pos_r)
    features.append(0 if not is_integer(token1) and not is_integer(token2) else 1)
    features.append(edit_distance(token1, token2))
    features.append(1 if token1 in token2 or token2 in token1 else 0)
    return features


def edit_distance(s1, s2):
    """ source: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/edit_distance_distance#Python
    """
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    find_synonyms_in_address()
