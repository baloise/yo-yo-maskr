import regex as re
import dill
import ahocorasick
from multiprocessing import Pool


class Anon:
    def __init__(self, names):
        self.pattern = re.compile(r'\b(' + '|'.join(map(re.escape, names)) + r')\b')
        self.automaton = ahocorasick.Automaton()
        for index, name in enumerate(names):
            self.automaton.add_word(name, (index, name))
        self.automaton.make_automaton()
        self.name_set = set(names)
        self._init_trie()

    def find_regex(self, text):
        return [(match.group(), match.start(), match.end()) for match in self.pattern.finditer(text)]

    def find_ahocorasick(self,text):
        # occurrences = []
        # for end_index, (idx, name) in self.automaton.iter(text):
        #     start_index = end_index - len(name) + 1
        #     occurrences.append((name, start_index, end_index))
        # return occurrences
        occurrences = []
        for end_index, (idx, name) in self.automaton.iter(text):
            start_index = end_index - len(name) + 1
            # Check if the match is an entire word using word boundaries
            if (start_index == 0 or not text[start_index - 1].isalnum()) and \
            (end_index == len(text) - 1 or not text[end_index + 1].isalnum()):
                occurrences.append((name, start_index, end_index))
        return occurrences
    
    def find_trie(self,text):
        firstnames = list(re.finditer(self.first_trie_regex, text, overlapped=True))
        lastnames = list(re.finditer(self.last_trie_regex, text, overlapped=True))
        return [(match.group(), match.start(), match.end()) for match in firstnames + lastnames]

    def _init_trie(self):        
        from src.utils.ano_regex import create_names_regex
        from src.utils.trie import Trie

        with open('./data/first_names_trie_regex.pkl', 'rb') as f:
            self.first_trie_regex = dill.load(f)
        with open('./data/last_names_trie_regex.pkl', 'rb') as f:
            self.last_trie_regex = dill.load(f)
    

    def find_set(self,text):
        occurrences = []
        for match in re.finditer(r'\b\w+\b', text):
            word = match.group()
            if word in self.name_set:
                occurrences.append((word, match.start(), match.end()))
        return occurrences

    def run_parallel(self, method, text, num_workers=4):
        from multiprocessing import Pool
        
        # Split text into lines
        lines = text.splitlines(keepends=True)
        total_lines = len(lines)
        chunk_size = total_lines // num_workers
        
        # Create chunks ensuring each line is entirely in one block
        chunks = []
        for i in range(num_workers):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i != num_workers - 1 else total_lines
            chunk = ''.join(lines[start_index:end_index])
            chunks.append(chunk)
        
        with Pool(num_workers) as pool:
            results = pool.map(method, chunks)
        return [item for sublist in results for item in sublist]

if __name__ == "__main__":
    with open('data/_all_orig.txt', 'r') as file:
        text = file.read()

    with open('data/first_names.txt', 'r') as names_file:
        names = {line.strip() for line in names_file}

    with open('data/last_names.txt', 'r') as names_file:
        lnames = {line.strip() for line in names_file}

    names.update(lnames)
    if '' in names:
        names.remove('')

    anon = Anon(names)
    
    def write_matches(matches, file):
        with open(f"tmp/{file}.txt", 'w') as file:
            file.write('\n'.join(repr(match) for match in matches))
    

    matches_trie = anon.find_trie(text)
    print(len(matches_trie))
    write_matches(matches_trie, 'matches_trie')
    

    matches_set = anon.find_set(text)
    print(len(matches_set))
    write_matches(matches_set, 'matches_set')

    
    matches_regex = anon.find_regex(text)
    print(len(matches_regex))
    write_matches(matches_regex, 'matches_regex')
    

    matches_aho = anon.find_ahocorasick(text)
    print(len(matches_aho))
    write_matches(matches_aho, 'matches_aho')



