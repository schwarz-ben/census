import os.path
import pandas as pd

DEFAULT_DATA_PATH = os.path.join("..","CensusIncome")
DEFAULT_DS_TRAIN_NAME = "adult.data"
DEFAULT_DS_TEST_NAME = "adult.test"


COLUMN_LABELS = [ "age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation",
          "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country",
          "50K"
        ]

def load_data(which=None,path=os.path.join( DEFAULT_DATA_PATH,DEFAULT_DS_TRAIN_NAME )):
    """ returns census data as a list of pandas DataFrames

    The optional 'which' parameter defines what data we want to load. Possible values are:
        - train: the trainset
        - test: the testset
        - combined: both trainset and testset as one file
        - all: all datasets are returned in this order: [combined, train, test]

    parameters
    :param str which: (optional) specifies the dataset to load ['all','train','test','combined'], if None, returns all
    :param path-like path: (optional)
    """

    df_train, df_test = None, None

    if which is None:
        which = "all"

    if which.lower() != 'test':
        df_train = pd.read_csv(
                    os.path.join(DEFAULT_DATA_PATH,DEFAULT_DS_TRAIN_NAME),
                    index_col=False,
                    engine="python", header=None, names=COLUMN_LABELS, sep=",", skipinitialspace=True,
                    #converters = { "50K": (lambda l: l==">50K")}
                    na_values="?"
                    )

    if which.lower() != 'train':
        df_test = pd.read_csv(
                    os.path.join(DEFAULT_DATA_PATH,DEFAULT_DS_TEST_NAME),
                    index_col=False,
                    engine="python", header=None, names=COLUMN_LABELS, sep=",", skipinitialspace=True,
                    converters = { "50K": (lambda l: l.rstrip("."))},
                    na_values="?",
                    skiprows=1
                    )
    lst=[]
    if which == "train" :
        return df_train
    elif which == "test" :
        return df_test
    else :
        lst = [df_train,df_test]

    df = pd.concat([df_train,df_test])

    if which == "combined":
        return [df]
    elif which == "all":
        return [df,df_train,df_test]
    else:
        raise ValueError("Can't make anything with 'which' value of ({})".format(which))



def test_load():
    df_list = load_data()
    print("read",len(df_list),"DataFrames")
    for i,df in enumerate(df_list):
        print(" i:",df.shape)


if __name__ == "__main__":
    test_load()
