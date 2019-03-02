import os
import json
import random
from IPython.display import Image, HTML, display

subject = None
data = None
img_path = None
mark_file = None
marked = []
qid = []
current_index = -1
answered = True
correct = 0
wrong = 0
skipped = 0


def select_subject(sub):
    global subject
    global data
    global img_path
    global mark_file
    global marked
    
    # reset state
    global qid
    global current_index
    global answered
    global correct
    global wrong
    global skipped
    qid = []
    current_index = -1
    answered = True
    correct, wrong, skipped = 0, 0, 0
    
    if sub == 1 or sub == '1':
        subject = 1
        with open(os.path.join('OS_ChineseDrivingTestQuestionBank', 'DATA_P1', 'data.json')) as f:
            dirty_json = f.read()
        for key in 'id question choices answer imageUrl imageUrlBig a b c d'.split():
            dirty_json = dirty_json.replace('{}:'.format(key), '"{}":'.format(key))
        dirty_json = dirty_json.replace("'", '"')
        data = json.loads(dirty_json[:-4] + ']')
        img_path = os.path.join('OS_ChineseDrivingTestQuestionBank', 'DATA_P1', 'imgBig')
        mark_file = 'marked_P1.txt'
    else:
        subject = 2
        with open(os.path.join('OS_ChineseDrivingTestQuestionBank', 'DATA_P2', 'data2.json')) as f:
            data = json.load(f)
        img_path = os.path.join('OS_ChineseDrivingTestQuestionBank', 'DATA_P2', 'images')
        mark_file = 'marked_P2.txt'
    try:
        with open(mark_file) as f:
            marked = [int(s) for s in f.read().split()]
    except FileNotFoundError:
        marked = []


def set_mode(mode, shuffle=False, max_count=10000, offset=0):
    global qid
    global current_index
    global answered
    
    current_index = -1
    answered = True
    
    if mode == 'all':
        qid = list(range(len(data)))
    elif mode == 'marked':
        qid = marked.copy()
    if shuffle:
        random.shuffle(qid)
    qid = qid[offset:(offset + max_count)]
    

def exam():
    set_mode('all', shuffle=True, max_count=100)
    
    
def show_stat():
    print('Correct: {}, Wrong: {}, Skipped: {}.'.format(correct, wrong, skipped))
    if correct + wrong + skipped != 0:
        print('Error rate: {:.1f}%'.format(wrong / (correct + wrong + skipped) * 100))
    

def next_question():
    global current_index
    global answered
    global skipped
    if not answered:
        skipped += 1
        answered = False
    if current_index < len(qid):
        current_index += 1
    if current_index >= len(qid):
        print("Congrats! You've finished!")
        show_stat()
    else:
        show()
        
        
def previous_question():
    global current_index
    if current_index >= 0:
        current_index -= 1
    if current_index < 0:
        print('You are already at the first question.')
    else:
        show()
        

def jump(to):
    global current_index
    if 0 <= to < len(qid):
        current_index = to
        show()
    else:
        print('Invalid index.')
        
        

def show():
    print('Question #{}'.format(qid[current_index]))
    q = data[qid[current_index]]
    if subject == 1:
        print(q['question'])
        for s in q['choices'].values():
            print(s)
        if q['imageUrlBig']:
            img_file = os.path.join(img_path, '{}.png'.format(q['id']))
            display(Image(img_file))
    else:
        display(HTML(q['question']))
        if q['img']:
            img_file = os.path.join(img_path, q['img'].split('/')[-1])
            display(Image(img_file))
            

def submit_answer(answer):
    global answered
    global correct
    global wrong
    
    answered = True
    
    q = data[qid[current_index]]
    if answer == 't':
        answer = 'a'
    if answer == 'f':
        answer = 'b'
    if answer == q['answer'].lower():
        ok = True
    elif q['answer'] == '×' and answer == 'b':
        ok = True
    elif (q['answer'] == '对' and answer == 'a') or (q['answer'] == '错' and answer == 'b'):
        ok = True
    else:
        ok = False
    if ok:
        print('Correct.')
        correct += 1
    else:
        print('Wrong. Correct answer: {}'.format(q['answer']))
        wrong += 1
    if subject == 2:
        print(q['explanation'])
        
        
def write_marked():
    with open(mark_file, 'w') as f:
        for i in marked:
            f.write('{}\n'.format(i))
            
        
def mark():
    if 0 <= current_index < len(qid):
        marked.append(qid[current_index])
        print('Marked question #{}'.format(qid[current_index]))
    write_marked()
        
        
def unmark():
    if 0 <= current_index < len(qid) and qid[current_index] in marked:
        marked.remove(current_index)
        print('Unmarked question #{}'.format(qid[current_index]))
    write_marked()
    
e = exam
s = show_stat
n = next_question
p = previous_question
m = mark
u = unmark
for answer in 'a b c d t f ab ac ad bc bd cd abc abd acd bcd abcd'.split():
    exec('''{0} = lambda: submit_answer("{0}")'''.format(answer))
    

select_subject(1)
set_mode('all')