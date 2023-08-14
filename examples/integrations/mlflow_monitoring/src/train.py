

def split_data(data, features, target, train_dates, test_dates):   
    print(f"train_end_data: {ref_end_data}") 
    X_train = data.loc[train_dates[0]:train_dates[1], features]
    y_train = data.loc[test_dates[0]:test_dates[1], target]
    print(X_train.shape, y_train.shape)
    
    current = data.loc[test_dates[0]:test_dates[1]]
    X_test = data.loc[test_dates[0]:test_dates[1]] features]
    y_test = current[target]
    print(X_test.shape, y_test.shape)
    
    return X_train, y_train, X_test, y_test