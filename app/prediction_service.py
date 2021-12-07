
from math import floor
from random import sample


class Assesment():
    # class var for lazy loading, thread safe?
    # corpus: Corpus = None

    questions = []
    sample_ratio = .01
    min_samples = 5

    step_breaks = {
        1: (1, 50),
        2: (51, 500),
        3: (501, 1000),
        4: (1001, 2000),
        5: (2001, 3000),
        6: (3001, 4000),
        7: (4001, 5000),
        8: (5001, 6000),
        9: (6001, 7000),
        10: (7001, 8000),
        11: (8001, 9000),
        12: (9001, 10000),
    }

    steps = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
    }

    def get_step_by_word(self, word):
        for key, value in self.step_breaks.items():
            if word.rank > value[0] and word.rank < value[1]:
                return key
        return None

    # def generate_questions(self):    
    #     print('generating questions')
    #     print(len(self.questions))
    #     for step_index, step_list in self.steps.items():
    #         choose_k = self.sample_size_for_set(step_index)
    #         ids = sample(list(step_list), choose_k)
    #         print(ids[0])
    #         for id in ids:
    #             self.questions.append(Question.from_word(self.corpus.vocab[id]))
    #     print(len(self.questions))

    def sort_corpus_to_sets(self):
        for word in self.corpus.vocab.values():
            step_index = self.get_step_by_word(word)
            if not step_index:
                continue
            self.steps[step_index].append(word.id)

    def sample_size_for_set(self, set_index):
        # returns the number of sample questions for set i based on the desired sampling ratio: self.sample_ratio

        #Get the size of the set and multiply by the ratio
        set_size = self.step_breaks[set_index][1] - self.step_breaks[set_index][0]
        sample_size = max(self.min_samples, floor(self.sample_ratio*set_size))
        return sample_size
    
    # @classmethod
    # def from_corpus(cls, corpus: Corpus):
    #     print('from corpus')
    #     return cls(corpus)
    #     # print(f'number of questions in assesment: {len(assesment.questions)}')
    #     # print(assesment)
    #     # return assesment


    # def __init__(self, corpus: Corpus, questions = None):
    #     # super().__init__(fname, lname)
    #     self.corpus = corpus
    #     if questions is None:
    #         self.questions = []
    #     else:
    #         self.questions = questions 
    #     self.sort_corpus_to_sets()
