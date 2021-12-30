
import itertools, random, math
from math import floor
from random import sample
from app.models import Question


class Assessment:
    ## possibly "offensive" words
    blacklist = ['e8f8a5ac-fcc3-4ad5-9dde-110be48a83ff', '0144aa8f-75ff-4257-873d-52ddb894ecbb', '3b24d1ef-ff45-4274-9b85-fe6c82d58cd5', 'fc9ee41b-405e-4d7e-aa45-87bc884e084d', 'c91e907d-6c0f-4e08-8c0b-5b072975a371']
    # class var for lazy loading, thread safe?
    # corpus: Corpus = None
    # v1 = V1()
    # step_breaks_list = [(1, 50), (51, 500), (501, 1000),(1001, 2000),(2001, 3000),(3001, 4000),(4001, 5000),(5001, 6000),(6001, 7000),(7001, 8000),(8001, 9000),(9001, 10000)]
    bin_size = 1000
    def __init__(self, questions: "list[Question]", ranks) -> None:
        self.sample_rate = .01
        self.questions = {question.vocab.uuid: question for question in questions}
        self.ranks = ranks
        self.bins, self.printable_bins = self.create_bins()
        self.questions = self.get_questions()
        self.prediction = self.assess()
        pass

    def get_sample_size(self, bin_index):
        first_num = bin_index*self.bin_size
        second_num = min((bin_index+1)*self.bin_size, self.ranks[-1][1])
        return math.floor((second_num - first_num + 1) * self.sample_rate)
    
    def create_bins(self):
        bins =[{'correct': [], 'total': [], 'choose': [], 'sample_size': self.get_sample_size(n)} for n in range(math.ceil(self.ranks[-1][1]/1000))]
        for rank in self.ranks:
            bin_index = math.ceil(rank[1]/1000) - 1
            if rank[0] in self.questions:
                bins[bin_index]['total'].append(rank[0])
                if self.questions[rank[0]].correct:
                    bins[bin_index]['correct'].append(rank[0])
            elif rank[0] not in self.blacklist:
                bins[bin_index]['choose'].append(rank[0])
        printable_bins = [{'correct': bin['correct'], 'total': bin['total'], 'choose': len(bin['choose']), 'sample_size': bin['sample_size']} for bin in bins]
        return bins, printable_bins

    def get_questions(self):
        question_vocab_uuids = []
        for bin in self.bins:
            choose_n = bin['sample_size'] - len(bin['total'])
            question_vocab_uuids.extend(random.sample(bin['choose'], choose_n))
        return question_vocab_uuids

    def assess(self):
        assessment = {
        'total_questioned': 0,
        'total_correct': 0,
        'total_predicted_correct': 0,
        'total_predicted_correct_naive': None,
        'data_length': len(self.ranks),
        }
        for bin in self.bins:
            assessment['total_questioned'] += len(bin['total'])
            assessment['total_correct'] += len(bin['correct'])

            if len(bin['total']) != 0 and assessment['total_predicted_correct'] != None:
                percentage_correct = len(bin['correct'])/len(bin['total'])
                predicted_correct = math.ceil(percentage_correct*self.bin_size)
                assessment['total_predicted_correct'] += predicted_correct
            else:
                assessment['total_predicted_correct'] = None
        if assessment['total_questioned'] > 0:
            assessment['total_predicted_correct_naive'] = math.floor((assessment['total_correct']/assessment['total_questioned'])*assessment['data_length'])
        return assessment
        
    def get_random_question_no_replacement(self):
        possible_indexes = [True for n in range(10000)]
        for rank in self.ranks:
            possible_indexes[rank - 1] = False
        possible_ranks = []
        for idx, val in enumerate(possible_indexes):
            possible_ranks.append(idx + 1)
        return random.choice(possible_ranks)

    def get_random_question_with_replacement(self):
        return random.randint(1, 10000)

    def get_assesment_question(self):
        return random.choice(self.questions)