import os.path
import pandas as pd

DEFAULT_DATA_PATH = os.path.join(".","CensusIncome")
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
    df.index = range(len(df.index))
    if which == "combined":
        return [df]
    elif which == "all":
        return [df,df_train,df_test]
    else:
        raise ValueError("Can't make anything with 'which' value of ({})".format(which))



def categorical_binner(rebinning_dictionnary,singletonToOther=False,labelOther="Other"):
    """ returns a function for rebinning a categorical variable

    :param dict rebinning_dictionnary: the dictionnary that will be used to map old labels to new ones
    :param boolean singletonToOther: (optional) if set to False (default) labels not found in the dictionnary
        are kept as is in the new categorical variable. If set to True, labels not found in the dictionnary
        are placed in a common "Other" category
    :param str labelOther: (optional) the label for the category "Other" if singletonToOther is set to True.
        Defaults to "Other".

    """
    def binner(x):
        try:
            return rebinning_dictionnary[x]
        except KeyError:
            return labelOther if singletonToOther else x
    return binner




def test_load():
    df_list = load_data()
    print("read",len(df_list),"DataFrames")
    for i,df in enumerate(df_list):
        print(" i:",df.shape)

    assert len(df_list[0].index.unique()) == len(df_list[0]),\
        "index of combined dataframe has redundant keys"

if __name__ == "__main__":
    test_load()
