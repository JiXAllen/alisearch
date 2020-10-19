import numpy as np
dataset_filename = "affinity_dataset.txt"
product = np.loadtxt(dataset_filename)
n_samples, n_features = product.shape
print("This dataset has {0} samples and {1} features".format(n_samples, n_features))

# 商品命名
features = ["bread", "milk", "cheese", "apples", "bananas"]

# 使用defaultdict，如果查找的键不存在，可返回一个默认值
# 统计量：“规则应验”、“规则无效”、“条件相同的规则”
from collections import defaultdict
valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurances = defaultdict(int)

# 前提：顾客购买了某一种商品
for sample in product:
    for premise in range(n_features):
        # 验证条件，不满足继续验证下一个条件
        if sample[premise] == 0: continue
        # 条件满足，出现次数加1。跳过条件和结论相同的情况
        num_occurances[premise] += 1
        for conclusion in range(n_features):
            if premise == conclusion: continue
            if sample[conclusion] == 1:
                valid_rules[(premise, conclusion)] += 1
            else:
                invalid_rules[(premise, conclusion)] += 1

# 支持度字典和置信度字典
support = valid_rules
confidence = defaultdict(float)
# keys函数以列表返回一个字典所有的键。
for premise, conclusion in valid_rules.keys():
    rule = (premise, conclusion)
    confidence[rule] = valid_rules[rule] / num_occurances[premise]

# 接收参数：前提条件和结论的特征索引值、支持度字典、置信度字典、特征列表
def print_rule(premise, conclusion, support, confidence, features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print("Rule: If a person buys {0}, they will also buy {1}".format(premise_name, conclusion_name))
    # 输出规则的支持度和置信度
    print(" - Support:{0}".format(support[(premise, conclusion)]))
    print(" - Confidence:{0:.3f}".format(confidence[(premise, conclusion)]))
    print("")
# 字典排序
# 按support排序
from operator import itemgetter
sorted_support = sorted(support.items(), key=itemgetter(1), reverse=True)
for index in range(5):
    print("rank by support")
    print("Rule #{0}".format(index+1))
    premise, conclusion = sorted_support[index][0]
    print_rule(premise, conclusion, support, confidence, features)

# 按confidence排序
sorted_confidence = sorted(confidence.items(), key=itemgetter(1), reverse=True)
for index in range(5):
    print("rank by confidence")
    print("Rule #{0}".format(index+1))
    premise, conclusion = sorted_support[index][0]
    print_rule(premise, conclusion, support, confidence, features)