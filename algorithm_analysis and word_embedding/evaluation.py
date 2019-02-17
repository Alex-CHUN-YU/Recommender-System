""" Reference from https://gist.github.com/bwhite/3726239
"""

import numpy as np
from functools import reduce

class Evaluation:
    def __init__(self):
        pass

    def dcg_at_k(self, r, k, method=0):
        """Score is discounted cumulative gain (dcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        >>> dcg_at_k(r, 1)
        3.0
        >>> dcg_at_k(r, 1, method=1)
        3.0
        >>> dcg_at_k(r, 2)
        5.0
        >>> dcg_at_k(r, 2, method=1)
        4.2618595071429155
        >>> dcg_at_k(r, 10)
        9.6051177391888114
        >>> dcg_at_k(r, 11)
        9.6051177391888114
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Discounted cumulative gain
        """
        r = np.asfarray(r)[:k]
        if r.size:
            if method == 0:
                return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
            elif method == 1:
                return np.sum(r / np.log2(np.arange(2, r.size + 2)))
            else:
                raise ValueError('method must be 0 or 1.')
        return 0.

    def ndcg_at_k(self, r, k, method=0):
        """Score is normalized discounted cumulative gain (ndcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        >>> ndcg_at_k(r, 1)
        1.0
        >>> r = [2, 1, 2, 0]
        >>> ndcg_at_k(r, 4)
        0.9203032077642922
        >>> ndcg_at_k(r, 4, method=1)
        0.96519546960144276
        >>> ndcg_at_k([0], 1)
        0.0
        >>> ndcg_at_k([1], 2)
        1.0
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Normalized discounted cumulative gain
        """
        # print("sorted:" + str(sorted(r, reverse=True)))
        dcg_max = self.dcg_at_k(sorted(r, reverse=True), k, method)
        # print("dcg_max:" + str(dcg_max))
        if not dcg_max:
            return 0.
        return self.dcg_at_k(r, k, method) / dcg_max

    def average_ndcg(self, r):
        """Relevance is positive real values.
        >>> r = [[3, 2, 3, 0, 0, 1, 2, 2, 3, 0],[2, 1, 1, 0, 0, 1, 2, 2, 3, 0]....[]]
        """
        scores = []
        score = []
        for rank_max in range(1, len(r[0]) + 1):
            score = []
            for data in r:
                score.append(self.ndcg_at_k(data[:rank_max], rank_max, method = 1))
            # 全部分數加起來在平均
            scores.append(reduce(lambda x, y: x + y, score) / len(score))
        return scores

    def average_precision(self, r, max_score):
        scores  = []
        score = []
        for rank_idx in range(0, len(r[0])):
            score = []
            for data in r:
                score.append(data[rank_idx])
            # 全部分數加起來除上總分
            scores.append(reduce(lambda x, y: x + y, score) / (len(score)*max_score))
        return scores

if __name__ == "__main__":
    e = Evaluation()
    # print(e.ndcg_at_k([0],5, method=1))
    # print(e.ndcg_at_k([1],5, method=1))
    # print(e.ndcg_at_k([1,0],5, method=1))
    # print(e.ndcg_at_k([0,1],5, method=1))
    # print(e.ndcg_at_k([0,1,1],5, method=1))
    # print(e.ndcg_at_k([0,1,1,1],6, method=1))
    # print(e.ndcg_at_k([2,1,1,1,1,0,1,0],5, method=1))
    # print(e.ndcg_at_k([2,1,1,1,1],5, method=1))
    print("Average NDCG Result:" + str(e.average_ndcg([[0, 2, 3, 0, 0, 1, 2, 2, 3, 0],[2, 1, 1, 0, 0, 1, 2, 2, 3, 0],[3, 2, 3, 0, 0, 1, 2, 2, 3, 0]])), end = '\n\n')
    print("Average Precision Result:" + str(e.average_precision([[3, 2, 3, 1, 0, 1, 2, 2, 3, 0],[2, 1, 1, 0, 0, 1, 2, 2, 3, 0],[3, 2, 3, 0, 0, 1, 2, 2, 3, 0]], 3)))