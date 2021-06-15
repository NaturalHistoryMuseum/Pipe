from sklearn.model_selection import train_test_split


def train_test(data, labels):
    x_train, x_test, y_train, y_test = train_test_split(data, labels,
                                                        test_size=0.2,
                                                        random_state=123, stratify=labels)
    return {
               'x': x_train,
               'y': y_train
               }, {
               'x': x_test,
               'y': y_test
               }
