#xác định tập biến
import itertools
def extractVars(clauses):
    vars_set = set()
    for clause in clauses:
        for literal in clause:
            if literal.startswith('-'):
                vars_set.add(literal[1:])
            else:
                vars_set.add(literal)
    return sorted(vars_set)
examples = [
    [['p', '-q'], ['q']],            
    [['-a', 'b', 'c'], ['-b'], ['d']], []
]

for cnf in examples:
    print("CNF:", cnf)
    print("Variables:", extractVars(cnf))
    print("---")
#mỗi biến nhận 2 giá trị True/False
def generate_interpretations(vars_list):
    n = len(vars_list)
    interpretations = []
    for bits in itertools.product([False, True], repeat=n):
        interpretation = dict(zip(vars_list, bits))
        interpretations.append(interpretation)
    return interpretations
var_exp = extractVars([['p', '-q'], ['q']])
all_interpretations = generate_interpretations(var_exp)
print(all_interpretations)
# kiểm tra công thức CNF với từng cách gán
def eval_literal(literal, interpretation):
    if literal.startswith('-'):
        return not interpretation.get(literal[1:], False)
    return interpretation.get(literal, False)
def eval_clause(clause, interpretation):
    return any(eval_literal(literal, interpretation) for literal in clause)
def eval_cnf(cnf, interpretation):
    return all(eval_clause(clause, interpretation) for clause in cnf)
cnf_example = [['p', '-q'], ['q']]
for interp in all_interpretations:
    result = eval_cnf(cnf_example, interp)
    print(f"{interp}, CNF: {result}")
#đánh giá công thức CNF với tất cả các cách gán biến, đếm
def analyze_cnf(cnf, show_model = False):
    for clauses in cnf:
        if len(clauses) == 0:
            return {
                'vars': [],
                'total_interpretations': 0,
                'models_count': 0,
                'models': [] if show_model else None,
                'status': 'unsatisfiable'
            }
    vars_list = extractVars(cnf) #lấy danh sách biến
    interpretations = generate_interpretations(vars_list) # sinh True/False
    total = len(interpretations)
    models = []
    for interp in interpretations:
        if eval_cnf(cnf, interp):
            models.append(interp.copy())
    models_count = len(models)
    
    if models_count == 0:
        status = 'unsatisfiable'
    elif models_count == total:
        status = 'true'  
    else:
        status = 'satisfiable'
    
    return {
        'vars': vars_list,
        'total_interpretations': total,
        'models_count': models_count,
        'models': models if show_model else None,
        'status': status
    }

examples = {
    "example1": [['p','-q'], ['q']],            # có 1 model
    "example2": [['p'], ['-p']],                # unsatisfiable (p and not p)
    "example3": [],                              # CNF rỗng -> true
    "example4": [['-a','b','c'], ['-b'], ['d']]  # kiểm tra nhiều biến
}

for name, cnf in examples.items():
    res = analyze_cnf(cnf, show_model=True)
    print(name, "-> status:", res['status'])
    print(" vars:", res['vars'])
    print(" total interpretations:", res['total_interpretations'])
    print(" models count:", res['models_count'])
    print(" models (shown):", res['models'])
    print("---")