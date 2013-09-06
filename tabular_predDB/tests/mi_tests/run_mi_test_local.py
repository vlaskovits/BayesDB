import itertools
import random
import numpy
import tabular_predDB.LocalEngine as LE
import tabular_predDB.python_utils.inference_utils as iu
import tabular_predDB.python_utils.mutual_information_test_utils as mitu

def run_mi_test_local(data_dict):

    gen_seed = data_dict['SEED']
    crosscat_seed = data_dict['CCSEED']
    num_clusters = data_dict['num_clusters']
    num_cols = data_dict['num_cols']
    num_rows = data_dict['num_rows']
    num_views = data_dict['num_views']
    corr = data_dict['corr']
    burn_in = data_dict['burn_in']
    mean_range = float(num_clusters)*2.0

    # 32 bit signed int
    random.seed(gen_seed)
    get_next_seed = lambda : random.randrange(2147483647)

    # generate the stats
    T, M_c, M_r, X_L, X_D = mitu.generate_correlated_state(num_rows,
        num_cols, num_views, num_clusters, mean_range, corr, seed=gen_seed);

    # get the original assignment
    view_assignment = numpy.array(X_L['column_partition']['assignments'])

    table_data = dict(T=T,M_c=M_c)

    engine = LE.LocalEngine(crosscat_seed)
    X_L_prime, X_D_prime = engine.analyze(M_c, T, X_L, X_D, n_steps=burn_in) 

    X_L = X_L_prime
    X_D = X_D_prime
 
    # for each view calclate the average MI between all pairs of columns
    n_views = len(X_D)
    MI = []
    Linfoot = []
    queries = []
    any_pairs = False
    for view in range(n_views):
        columns_in_view = numpy.nonzero(view_assignment==view)[0]
        combinations = itertools.combinations(columns_in_view,2)
        for pair in combinations:
            any_pairs = True
            queries.append(pair)
            MI_i, Linfoot_i = iu.mutual_information(M_c, [X_L], [X_D], [pair], n_samples=1000)
            MI.append(MI_i[0][0])

    if not any_pairs:
        MI = [0]

    ret_dict = dict(
        id=data_dict['id'],
        dataset=data_dict['dataset'],
        sample=data_dict['sample'],
        mi=MI,
        )

    return ret_dict