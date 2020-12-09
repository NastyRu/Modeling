import numpy.random as rn


dict = {'refusal_percentage': 0,
           'refusals': 0,
           'Mask': 0,
           'Temp': 0,
           'Ticket': 0,
           'Food': 0,
           'Controller': 0}


class RandomGenerator:
    def __init__(self, begin, delta=0):
        self.begin = begin
        self.d = delta

    def new_random(self):
        if (self.d == 0):
            return self.begin
        return rn.uniform(self.begin - self.d, self.begin + self.d)


class GenerateRequest:
    def __init__(self, generator, count):
        self.random_generator = generator
        self.num_requests = count
        self.receivers = []
        self.next = 0

    def generate_request(self):
        self.num_requests -= 1
        for receiver in self.receivers:
            if receiver.free:
                receiver.receive_request()
                return receiver

        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None

    def delay(self):
        t = -1
        while (t < 0):
            t = self.random_generator.new_random()
        return t


class ProcessRequest:
    def __init__(self, generator, name, max_queue=-1, end=False, p=0):
        self.random_generator = generator
        self.queue, self.max_queue, self.processed = 0, max_queue, 0
        self.next = 0
        self.name = name
        self.receivers = []
        self.end = end
        self.free = True
        self.p = p

    def receive_request(self):
        self.free = False
        if rn.random_sample() < self.p:
            dict[self.name] += 1
            return False
        if self.max_queue == -1 or self.max_queue > self.queue:
            self.queue += 1
            return True
        return False

    def process_request(self):
        self.processed += 1
        if self.queue > 0:
            self.queue -= 1
        else:
            self.free = True

        for receiver in self.receivers:
            if receiver.free:
                receiver.receive_request()
                return receiver
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver

        if (self.name == 'Mask'):
            dict['Temp'] += 1
        elif (self.name == 'Temp'):
            dict['Ticket'] += 1
        elif (self.name == 'Ticket'):
            dict['Food'] += 1
        elif (self.name == 'Food'):
            dict['Controller'] += 1
        return None

    def delay(self):
        return self.random_generator.new_random()


class Model:
    def __init__(self, generator, mask_operator, temp_operators, ticket_operator, food_operators, controller_operators):
        self.generator = generator
        self.mask_operator = mask_operator
        self.temp_operators = temp_operators
        self.ticket_operator = ticket_operator
        self.food_operators = food_operators
        self.controller_operators = controller_operators

    def event_mode(self):
        generated_requests = self.generator.num_requests
        generator = self.generator

        generator.receivers = [self.mask_operator]
        self.mask_operator.receivers = [self.temp_operators[0], self.temp_operators[1]]
        self.temp_operators[0].receivers = [self.ticket_operator]
        self.temp_operators[1].receivers = [self.ticket_operator]
        self.ticket_operator.receivers = [self.food_operators[0], self.food_operators[1], self.food_operators[2], self.controller_operators[0], self.controller_operators[1]]
        self.food_operators[0].receivers = [self.controller_operators[0]]
        self.food_operators[1].receivers = [self.controller_operators[0]]
        self.food_operators[2].receivers = [self.controller_operators[1]]

        generator.next = generator.delay()
        self.mask_operator.next = self.mask_operator.delay()

        blocks = [generator,
                  self.mask_operator,
                  self.temp_operators[0],
                  self.temp_operators[1],
                  self.ticket_operator,
                  self.food_operators[0],
                  self.food_operators[1],
                  self.food_operators[2],
                  self.controller_operators[0],
                  self.controller_operators[1]]

        dict['refusals'] = 0
        dict['Mask'] = 0
        dict['Temp'] = 0
        dict['Ticket'] = 0
        dict['Food'] = 0
        dict['Controller'] = 0

        while (self.controller_operators[0].processed + self.controller_operators[1].processed) < 100:
            current_time = generator.next
            for block in blocks:
                if 0 < block.next < current_time:
                    current_time = block.next

            for block in blocks:
                if current_time == block.next:
                    if not isinstance(block, ProcessRequest):
                        next_generator = generator.generate_request()
                        if next_generator is not None:
                            next_generator.next = current_time + next_generator.delay()
                        else:
                            dict['refusals'] += 1
                        generator.next = current_time + generator.delay()
                    else:
                        next_receiver = block.process_request()
                        if block.queue == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.delay()

                        if (block.end):
                            continue
                        if next_receiver is not None:
                            next_receiver.next = current_time + next_receiver.delay()
                        else:
                            dict['refusals'] += 1

        dict['refusal_percentage'] = dict['refusals'] / generated_requests * 100
        return dict


if __name__ == '__main__':
    per = []
    ref = []
    ref_mask = []
    ref_temp = []
    ref_ticket = []
    ref_food = []
    ref_controller = []

    for i in range(10):
        clients_number = 100

        generator = GenerateRequest(RandomGenerator(10, 5), clients_number)
        mask_operator = ProcessRequest(RandomGenerator(0, 1), 'Mask', max_queue=1, p=0.1)

        temp_operators = [ProcessRequest(RandomGenerator(2, 1), 'Temp', max_queue=0, p=0.05),
                          ProcessRequest(RandomGenerator(2, 1), 'Temp', max_queue=0, p=0.05)]

        ticket_operator = ProcessRequest(RandomGenerator(7, 5), 'Ticket', max_queue=3)

        food_operators = [ProcessRequest(RandomGenerator(5, 5), 'Food', max_queue=2),
                          ProcessRequest(RandomGenerator(3, 2), 'Food', max_queue=2),
                          ProcessRequest(RandomGenerator(5, 2), 'Food', max_queue=2)]

        controller_operators = [ProcessRequest(RandomGenerator(2, 2), 'Controller', max_queue=-1, end=True),
                                ProcessRequest(RandomGenerator(2, 2), 'Controller', max_queue=-1, end=True)]

        model = Model(generator, mask_operator, temp_operators, ticket_operator, food_operators, controller_operators)
        result = model.event_mode()

        per.append(result['refusal_percentage'])
        ref.append(result['refusals'])
        ref_mask.append(result['Mask'])
        ref_temp.append(result['Temp'])
        ref_ticket.append(result['Ticket'])
        ref_food.append(result['Food'])
        ref_controller.append(result['Controller'])

    print(f'Процент отказа в обработке: ({round(min(per), 3)}, {round(max(per), 3)})\n',
        f'Отказы: ({min(ref)}, {max(ref)})\n',
        f'Отказы на контроле маски: ({min(ref_mask)}, {max(ref_mask)})\n',
        f'Отказы на проверке температуры: ({min(ref_temp)}, {max(ref_temp)})\n',
        f'Отказы в покупке билетов: ({min(ref_ticket)}, {max(ref_ticket)})\n',
        f'Отказы в покупке еды: ({min(ref_food)}, {max(ref_food)})\n',
        f'Отказы в проверке билетов: ({min(ref_controller)}, {max(ref_controller)})\n')
