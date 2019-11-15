'''
Escalator Simulator

'''
import random

class Escalator:
    def __init__(self,
                 left_steps=[],
                 right_steps=[],
                 speed=1,
                 height=30):

        self.left_steps = left_steps;
        self.right_steps = right_steps;
        self.speed = speed;
        self.height = height;

    def add_step(self, step, side=''):
        if side.lower() == 'left':
            self.left_steps.append(step)
        if side.lower() == 'right':
            self.right_steps.append(step)

    def print_escalator(self):
        for i in range(self.height, 0, -1):
            print(' {} | {} '.format(self.left_steps[i-1].print_step(),
                                     self.right_steps[i-1].print_step()))

    def add_people(self, waiting_left, waiting_right):
        if waiting_left.is_empty():
            pass
        # adding standing person to first step
        elif waiting_left.get(0).walking_speed == 0 and not self.left_steps[0].is_occupied():
            self.left_steps[0].add_person(waiting_left.remove_person())
        # adding walking person to first step
        elif (waiting_left.get(0).walking_speed > 0 and
              not self.left_steps[0].is_occupied() and
              not self.left_steps[1].is_occupied()):
            self.left_steps[0].add_person(waiting_left.remove_person())

        if waiting_right.is_empty():
            pass
        # adding standing person to first step
        elif waiting_right.get(0).walking_speed == 0 and not self.right_steps[0].is_occupied():
            self.right_steps[0].add_person(waiting_right.remove_person())
        # adding walking person to first step
        elif (waiting_right.get(0).walking_speed > 0 and
              not self.right_steps[0].is_occupied() and
              not self.right_steps[1].is_occupied()):
            self.right_steps[0].add_person(waiting_right.remove_person())

        return (waiting_left, waiting_right)

    def remove_people(self, side=''):
        if side == 'right':
            top = self.right_steps[-1]
            second = self.right_steps[-2]
        elif side == 'left':
            top = self.left_steps[-1]
            second = self.left_steps[-2]

        if top.is_occupied():
            return top.remove_person()
        elif second.is_occupied() and second.occupant_speed() > 0:
            return second.remove_person()
        else:
            return None

    def move_people(self, side=''):
        if side == 'right':
            steps = self.right_steps
        elif side == 'left':
            steps = self.left_steps

        for i in range(self.height-1, 0, -1):
            i -=1
            if steps[i].is_occupied():
                total_speed = self.speed + steps[i].occupant_speed()
                next_step = i + total_speed

                if next_step > len(steps)-1:
                    next_step = len(steps)-1

                if total_speed > self.speed and next_step == len(steps)-1:
                    # move to step is the person is walking and the last step is free
                    if not steps[next_step].is_occupied:
                        steps[next_step].add_person(steps[i].remove_person())

                elif total_speed > self.speed and (not steps[next_step+1].is_occupied()):
                    # move to step is the person is walking and the step after the next is free
                    if not steps[next_step].is_occupied():
                        steps[next_step].add_person(steps[i].remove_person())

                # move a standing person to the next step
                elif total_speed == self.speed and (not steps[next_step].is_occupied()):
                        steps[next_step].add_person(steps[i].remove_person())


    def move_escalator(self, side=''):
        finished_people = [self.remove_people(side='left'),
                           self.remove_people(side='right')]

        self.move_people(side='left')
        self.move_people(side='right')

        return finished_people

class Step:
    def __init__(self, occupied=None):
        self.occupied = occupied;

    def add_person(self, p):
        self.occupied = p;

    def is_occupied(self):
        return bool(self.occupied)

    def occupant_speed(self):
        return int(self.occupied.walking_speed)

    def remove_person(self):
        p = self.occupied;
        self.occupied = None;
        return p;

    def print_step(self):
        if self.occupied:
            return str(self.occupied.id)
        else:
            return '-'

class Person:
    def __init__(self, id=0, walking_speed=0):
        self.id = id;
        self.walking_speed = walking_speed;

class Queue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return bool(not self.queue)

    def add_person(self, p):
        self.queue.append(p)

    def remove_person(self):
        return self.queue.pop(0)

    def get(self, index):
        return self.queue[index]

    def print_queue(self):
        for p in self.queue:
            print('Person: {} walks at speed {}'.format(p.id, p.walking_speed))

def main():
    people = 100
    height = 20
    # create Escalator with 30 steps
    e = Escalator(height=height)
    for i in range(height):
        e.add_step(Step(), side='left')
        e.add_step(Step(), side='right')

    # generate random queue with 100 people equally distributed between two lanes
    waiting_right = Queue()
    waiting_left = Queue()
    finished = set()
    for i in range(people):
        random_speed = int(random.getrandbits(1))
        if (i < 50):
            waiting_right.add_person(Person(id=i, walking_speed=random_speed))
        else:
            waiting_left.add_person(Person(id=i, walking_speed=random_speed))

    waiting_right.print_queue()
    waiting_left.print_queue()

    number_of_moves = 0

    while len(finished) < people:
        number_of_moves += 1

        waiting_left, waiting_right = e.add_people(waiting_left, waiting_right)
        resp = e.move_escalator()
        e.print_escalator()
        for x in resp:
            if x:
                finished.add(x)
        print('-----------------')

    print(number_of_moves)

if __name__ == '__main__':
    main()
